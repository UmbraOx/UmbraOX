from core.runtime.runtime_agent_router import RuntimeAgentRouter


def test_runtime_agent_router():

    router = RuntimeAgentRouter()

    result = router.route(
        "coder",
        "build module"
    )

    assert result["status"] == "routed"