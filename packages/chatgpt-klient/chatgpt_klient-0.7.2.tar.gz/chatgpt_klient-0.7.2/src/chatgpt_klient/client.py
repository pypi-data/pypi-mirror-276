import copy
from openai import OpenAI, AzureOpenAI
from openai import RateLimitError, APITimeoutError, BadRequestError
import math
import time
import tiktoken
from typing import Generator, Union, Literal, Dict
from logutils import get_logger
from chatgpt_klient.consts import (
    MAX_DELAY,
    ENGINES,
    DEFAULT_ENGINES,
    CLIENT_TIMEOUT,
    DEFAULT_AZURE_API_VERSION,
    DEFAULT_AZURE_ENDPOINT,
)
from chatgpt_klient.exceptions import (
    InvalidModelError,
    InvalidResponseError,
)
from rich.console import Console

logger = get_logger("chatgpt_client")
console = Console()


class LLMClient:
    def __init__(
        self,
        api_key,
        model: str | Dict = "gpt3.5-default",
        cap_tokens=math.inf,
        service: Literal["openai", "azure", "openai-compatible"] = "openai",
        azure_api_version: str = DEFAULT_AZURE_API_VERSION,
        azure_endpoint: str = DEFAULT_AZURE_ENDPOINT,
        azure_instance: str | None = None,
        openai_endpoint: str | None = None,
        insecure_mode: bool = False,
    ):
        # Initialize some attributes
        self.api_key = api_key
        self.service = service
        self.msg_history = {"messages": [], "tokens": []}
        self.last_prompt_tokens = 0
        self.cap_tokens = cap_tokens
        self.insecure_mode = insecure_mode
        if isinstance(model, Dict):
            self.model_name = model["name"]
            model_definition = model
        else:
            self.model_name = model
            if self.model_name in DEFAULT_ENGINES.keys():
                self.model_name = DEFAULT_ENGINES[self.model_name]
            for k, v in ENGINES.items():
                if k == self.model_name:
                    model_definition = v
                    break
            else:
                if not self.insecure_mode:
                    raise Exception(f"Model {self.model_name} not found")

        if self.insecure_mode:
            self.type = None
            self.model_max_output_tokens = None
            self.model_max_tokens = None
        else:
            self.type = model_definition["type"]
            self.model_max_tokens = model_definition["max_tokens"]
            if "max_output_tokens" in model_definition:
                self.model_max_output_tokens = model_definition["max_output_tokens"]
                self.max_tokens = self.model_max_tokens - self.model_max_output_tokens
            else:
                self.model_max_output_tokens = self.model_max_tokens
                self.max_tokens = int(self.model_max_tokens / 2)

            if service in ("openai", "azure"):
                self.tokenizer = tiktoken.encoding_for_model(self.model_name)
                self.encode = self.tokenizer.encode
            else:
                from transformers import AutoTokenizer
                from huggingface_hub import login

                try:
                    login(model_definition["hf_token"])
                    self.tokenizer = AutoTokenizer.from_pretrained(
                        model_definition["base_model"]
                    )
                    self.encode = self.tokenizer.tokenize
                except Exception:
                    self.tokenizer = tiktoken.get_encoding(model_definition["encoding"])

        self.azure_instance = None
        if self.service == "azure":
            if azure_instance is None:
                raise NoAzureInstanceError("Azure API requires passing an instance")
            self.model_name = azure_instance
            self.azure_instance = azure_instance

        # Initialize the OpenAI/Azure/OpenAI-compatible engine
        if self.service == "openai":
            logger.info(f"Initializing an OpenAI {self.model_name} engine")
            self.openai = OpenAI(api_key=self.api_key, timeout=CLIENT_TIMEOUT)
        elif self.service == "azure":
            if azure_instance is None:
                raise NoAzureInstanceError
            logger.info(
                f"Initializing an Azure connection to the {azure_instance} instance (model {self.model_name})"
            )
            self.openai = AzureOpenAI(
                api_key=self.api_key,
                api_version=azure_api_version,
                azure_endpoint=azure_endpoint,
            )
        elif self.service == "openai-compatible":
            logger.info(
                f"Initializing an OpenAI-compatible {self.model_name} engine with endpoint {openai_endpoint}"
            )
            self.openai = OpenAI(
                api_key=self.api_key,
                base_url=openai_endpoint,
                timeout=CLIENT_TIMEOUT,
            )

        if not self.insecure_mode:
            self.check_model_validity()

    def check_model_validity(self):
        try:
            if self.type == "legacy":
                r = self.openai.completions.create(
                    model=self.model_name,
                    prompt="Hi",
                    max_tokens=5,
                ).model_dump()
                r = self.check_response_validity(r)
            elif self.type == "chat":
                r = self.openai.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=5,
                ).model_dump()
                r = self.check_response_validity(r)
                logger.debug(
                    f'Model validity test: {r["choices"][0]["message"]["content"]}'
                )
            else:
                raise InvalidModelError(f"Engine {self.model_name} not supported")
        except Exception:
            logger.exception(f"Invalid model ({self.model_name}) for your API key")
            raise InvalidModelError(f"Engine {self.model_name} not supported")
        else:
            logger.info(f"Model ({self.model_name}) and API key seem to be valid.")

    def check_response_validity(self, r) -> dict:
        try:
            match r:
                case {"choices": [{"text": str()}]}:
                    pass
                case {"choices": [{"message": {"content": str()}}]}:
                    pass
                case _:
                    raise InvalidModelError
        except Exception:
            raise InvalidResponseError(f"Response is not well formed: {r}")
        else:
            logger.debug("Response seems to be well formed")
            return r

    def set_system_directive(self, directive: str):
        self.clean_history(keep_sysdir=False)
        self.msg_history["messages"].append(
            {
                "role": "system",
                "content": directive,
            }
        )
        self.msg_history["tokens"].append(len(self.tokenizer.encode(directive)))

    def clean_history(self, keep_sysdir=True):
        new_history = {"messages": [], "tokens": []}
        if keep_sysdir:
            for i, m in enumerate(self.msg_history["messages"]):
                if m["role"] == "system":
                    new_history["messages"].append(
                        {"role": m["role"], "content": m["content"]}
                    )
                    new_history["tokens"].append(self.msg_history["tokens"][i])
        self.msg_history = new_history
        self.last_prompt_tokens = 0

    def get_max_tokens_allowed(self):
        return (
            min(
                [
                    self.max_tokens,
                    self.model_max_tokens or math.inf,
                    self.cap_tokens,
                ]
            )
            - 10
        )

    def calculate_prompt_tokens(self, text, no_history=True, keep_sysdir=False):
        aux_history = copy.deepcopy(self.msg_history)
        aux_last_prompt = self.last_prompt_tokens
        if no_history:
            self.clean_history(keep_sysdir=keep_sysdir)
        self.msg_history["messages"].append(
            {
                "role": "user",
                "content": text,
            }
        )
        self.msg_history["tokens"].append(len(self.tokenizer.encode(text)))
        potential_tokens = self.msg_history["tokens"][-1] + self.last_prompt_tokens
        self.msg_history = aux_history
        self.last_prompt_tokens = aux_last_prompt
        return potential_tokens

    def send_prompt(
        self, text: str, no_history: bool = False, stream: bool = False
    ) -> Union[str, Generator[str, None, None]]:
        """
        Send a prompt to ChatGPT with some text to get a response.

        :param text: the text to be sent as a prompt. This will be appended as the
          latest "user" message of the conversation
        :param no_history: deactivate the use of a previous history of messages. If
          set to True, all previous messages will be cleared and only the one in
          *text* will be used
        :param stream: set to True to return the generated tokens synchronously, one
          by one as we receive them from ChatGPT. Otherwise, the text will be returned
          as a whole once it is ready.
        :returns: either a string with the whole text, or a generator of the tokens
          composing the text
        """
        response = "No response"
        if self.type == "legacy":
            r = self.openai.completions.create(
                model=self.model_name,
                prompt=text,
                max_tokens=self.model_max_output_tokens,
            ).model_dump()
            r = self.check_response_validity(r)
            response = r["choices"][0]["text"]
        elif self.type == "chat" or (self.type is None and self.insecure_mode):
            if no_history:
                self.clean_history()
            self.msg_history["messages"].append(
                {
                    "role": "user",
                    "content": text,
                }
            )
            if not self.insecure_mode:
                self.msg_history["tokens"].append(len(self.tokenizer.encode(text)))
                self.reduce_msg_history(text)
            if stream:
                return self.chat_completion_stream(text)
            else:
                return self.chat_completion_no_stream(text)
        else:
            logger.warning(f"Engine {self.model_name} not supported")
        return response

    def interactive_prompt(self, system_directive: str | None = None):
        if system_directive:
            self.set_system_directive(system_directive)
        console.print("###########", style="bold")
        console.print("# ChatGPT #", style="bold")
        console.print("###########", style="bold")
        console.print(
            f"[bold yellow]Engine:[/bold yellow] {self.model_name}", highlight=False
        )
        console.print("[bold cyan]Enter 'q'/'quit' to exit the chat[/]")
        console.print("[bold cyan]Enter anything to start chatting.[/]")
        console.print()
        while True:
            input_text = input("$ ")
            if input_text in ("q", "quit"):
                print("ChatGPT> Sayonara, baby!")
                break
            try:
                r = self.send_prompt(text=input_text)
            except RateLimitError:
                logger.warning("You are sending requests too fast. Delaying 20s...")
                time.sleep(20)
                r = self.send_prompt(text=input_text)

            console.print(f"[bold green]ChatGPT>[/] [green]{r}[/]")

    def reduce_msg_history(self, text: str):
        potential_tokens = self.msg_history["tokens"][-1] + self.last_prompt_tokens
        logger.debug(f"Potential tokens: {potential_tokens}")
        while potential_tokens > self.get_max_tokens_allowed():
            logger.warning("Too many tokens. Reducing history size")
            aux = {"messages": [], "tokens": []}
            first_user = True
            first_assistant = True
            for i in range(len(self.msg_history["messages"])):
                if self.msg_history["messages"][i]["role"] == "user" and first_user:
                    first_user = False
                    potential_tokens -= self.msg_history["tokens"][i]
                elif (
                    self.msg_history["messages"][i]["role"] == "assistant"
                    and first_assistant
                ):
                    first_assistant = False
                    potential_tokens -= self.msg_history["tokens"][i]
                else:
                    aux["messages"].append(self.msg_history["messages"][i])
                    aux["tokens"].append(self.msg_history["tokens"][i])
            self.msg_history = aux
        if text not in [m["content"] for m in self.msg_history["messages"]]:
            raise TooManyTokensError(
                f"The maximum accepted tokens ({self.get_max_tokens_allowed()}) is not big enough to process your prompt"
            )

    def chat_completion_no_stream(self, text: str, delay: int = 5) -> str:
        try:
            r = self.openai.chat.completions.create(
                model=self.model_name,
                messages=self.msg_history["messages"],
                max_tokens=self.model_max_output_tokens,
                stream=False,
            ).model_dump()
            logger.debug(r)
            r = self.check_response_validity(r)
            self.last_prompt_tokens = r["usage"]["total_tokens"]
            response = r["choices"][0]["message"]["content"]
            if response:
                self.msg_history["messages"].append(
                    {
                        "role": "assistant",
                        "content": response,
                    }
                )
                if not self.insecure_mode:
                    self.msg_history["tokens"].append(
                        len(self.tokenizer.encode(response))
                    )
        except RateLimitError:
            logger.warning(f"Rate limit reached, delaying request {delay} seconds")
            if delay > MAX_DELAY:
                raise Exception(
                    "Recurring RateLimitError and delaying requests not working"
                )
            time.sleep(delay)
            return self.chat_completion_no_stream(text, delay=delay * 2)
        except BadRequestError as e:
            if "maximum context length" in str(e):
                self.clean_history(keep_sysdir=True)
                return self.chat_completion_no_stream(text, delay=delay * 2)
            else:
                logger.warning("We shouldn't be getting here!")
                raise e
        except APITimeoutError:
            logger.warning("Request failed with timeout, retrying")
            if delay > MAX_DELAY:
                raise Exception("Getting timeouts to all requests")
            time.sleep(delay)
            return self.chat_completion_no_stream(text, delay=delay * 2)
        else:
            return response

    def chat_completion_stream(
        self, text: str, delay: int = 5
    ) -> Generator[str, None, None]:
        try:
            stream = self.openai.chat.completions.create(
                model=self.model_name,
                messages=self.msg_history["messages"],
                max_tokens=self.model_max_output_tokens,
                stream=True,
            )
            aux_num_tokens = 0
            aux_text = ""
            for r in stream:
                match chunk := r.choices[0].model_dump():
                    case {"finish_reason": "stop"}:
                        break
                    case {"delta": {"content": token}}:
                        logger.debug(f"Received chunk: {token}")
                        aux_text += token
                        aux_num_tokens += 1
                        yield token
                    case _:
                        logger.warning(f"Strange object structure: {chunk}")
            self.last_prompt_tokens = aux_num_tokens
            self.msg_history["messages"].append(
                {
                    "role": "assistant",
                    "content": aux_text,
                }
            )
            if not self.insecure_mode:
                self.msg_history["tokens"].append(len(self.tokenizer.encode(aux_text)))
        except RateLimitError:
            logger.warning(f"Rate limit reached, delaying request {delay} seconds")
            if delay > MAX_DELAY:
                raise Exception(
                    "Recurring RateLimitError and delaying requests not working"
                )
            time.sleep(delay)
            self.chat_completion_stream(text, delay=delay * 2)
        except BadRequestError as e:
            if "maximum context length" in str(e):
                self.clean_history(keep_sysdir=True)
                self.chat_completion_stream(text, delay=delay * 2)
            else:
                logger.warning("We shouldn't be getting here!")
                raise e
        except APITimeoutError:
            logger.warning("Request failed with timeout, retrying")
            if delay > MAX_DELAY:
                raise Exception("Getting timeouts to all requests")
            time.sleep(delay)
            self.chat_completion_stream(text, delay=delay * 2)


class TooManyTokensError(Exception):
    pass


class NoAzureInstanceError(Exception):
    pass
