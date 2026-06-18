from core.runtime.runtime_agent_dispatcher import RuntimeAgentDispatcher


def test_runtime_agent_dispatcher():
    dispatcher = RuntimeAgentDispatcher()

    result = dispatcher.dispatch("build module")

    assert result["status"] == "assigned"