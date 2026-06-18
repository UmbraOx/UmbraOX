from core.runtime.runtime_prompt_runtime import RuntimePromptRuntime


def test_runtime_prompt_runtime():
    runtime = RuntimePromptRuntime()

    result = runtime.submit_prompt("build runtime")

    assert result["status"] == "success"