from core.runtime.runtime_live_prompt_session import RuntimeLivePromptSession


def test_runtime_live_prompt_session():
    session = RuntimeLivePromptSession()

    result = session.run_prompt("build autonomous planner")

    assert result["status"] == "success"