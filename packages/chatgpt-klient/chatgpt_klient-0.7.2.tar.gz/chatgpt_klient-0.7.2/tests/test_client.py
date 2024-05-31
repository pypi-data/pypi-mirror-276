import pytest
import json
from chatgpt_klient.consts import ROOT_DIR, ENGINES, DEFAULT_ENGINES, OLLAMA_ENGINES
from chatgpt_klient.client import LLMClient


@pytest.fixture
def config():
    config_f = ROOT_DIR.joinpath("config.json")
    return json.loads(config_f.read_text())


@pytest.mark.parametrize("model", ENGINES.keys())
def test_LLMClient_init_all_models_OK(model, config):
    if model in OLLAMA_ENGINES:
        LLMClient(
            service="openai-compatible",
            api_key=config["poligpt_key"],
            openai_endpoint=config["poligpt_endpoint"],
            model=model,
        )
    else:
        LLMClient(service="openai", api_key=config["openai_key"], model=model)


@pytest.mark.parametrize("model", DEFAULT_ENGINES.keys())
def test_LLMClient_init_default_models_OK(model, config):
    LLMClient(api_key=config["openai_key"], model=model)


def test_LLMClient_init_nomodel_OK(config):
    LLMClient(api_key=config["openai_key"])


@pytest.mark.parametrize("model", ["gpt4", "ronaldo"])
def test_LLMClient_init_bad_model_FAIL(model, config):
    with pytest.raises(Exception):
        LLMClient(api_key=config["openai_key"], model=model)


@pytest.mark.parametrize("model", DEFAULT_ENGINES.keys())
def test_LLMClient_init_bad_apikey_FAIL(model):
    with pytest.raises(Exception):
        LLMClient(api_key="roberta", model=model)


@pytest.mark.parametrize("model", DEFAULT_ENGINES.keys())
def test_send_prompt(model, config):
    prompter = LLMClient(api_key=config["openai_key"], model=model)
    r = prompter.send_prompt("hola caracola")
    print(f"Response: {r}")
    assert isinstance(r, str)


@pytest.mark.parametrize("model", DEFAULT_ENGINES.keys())
def test_send_prompt_streaming(model, config):
    prompter = LLMClient(api_key=config["openai_key"], model=model)
    r = prompter.send_prompt("hola caracola", stream=True)
    for token in r:
        assert isinstance(token, str)
