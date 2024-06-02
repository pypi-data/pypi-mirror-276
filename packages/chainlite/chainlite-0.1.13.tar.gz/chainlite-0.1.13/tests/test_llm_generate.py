import pytest

from chainlite import llm_generation_chain, load_config_from_file
from chainlite.llm_config import GlobalVars
from chainlite.llm_generate import write_prompt_logs_to_file
from chainlite.utils import get_logger
from langchain_core.runnables import RunnableLambda

logger = get_logger(__name__)


# load_config_from_file("./llm_config.yaml")


@pytest.mark.asyncio(scope="session")
async def test_llm_generate():
    # Check that the config file has been loaded properly
    assert GlobalVars.all_llm_endpoints
    assert GlobalVars.prompt_dirs
    assert GlobalVars.prompt_log_file
    # assert GlobalVars.prompts_to_skip_for_debugging
    assert GlobalVars.local_engine_set

    response = await llm_generation_chain(
        template_file="test.prompt",  # prompt path relative to one of the paths specified in `prompt_dirs`
        engine="gpt-35-turbo",
        max_tokens=100,
    ).ainvoke({})
    # logger.info(response)

    assert response is not None, "The response should not be None"
    assert isinstance(response, str), "The response should be a string"
    assert len(response) > 0, "The response should not be empty"


@pytest.mark.asyncio(scope="session")
async def test_readme_example():
    response = await llm_generation_chain(
        template_file="tests/joke.prompt",
        engine="gpt-35-turbo",
        max_tokens=100,
        temperature=0.1,
        progress_bar_desc="test1",
        additional_postprocessing_runnable=RunnableLambda(lambda x: x[:5]),
    ).ainvoke({"topic": "Life as a PhD student"})


@pytest.mark.asyncio(scope="session")
async def test_batching():
    chain_inputs = [
        {"topic": "Ice cream"},
        {"topic": "Cats"},
        {"topic": "Dogs"},
        {"topic": "Rabbits"},
    ]
    response = await llm_generation_chain(
        template_file="tests/joke.prompt",
        engine="gpt-35-turbo",
        max_tokens=100,
        temperature=0.1,
        progress_bar_desc="test2",
    ).abatch(chain_inputs)
    assert len(response) == len(chain_inputs)

    write_prompt_logs_to_file("tests/llm_input_outputs.jsonl")
