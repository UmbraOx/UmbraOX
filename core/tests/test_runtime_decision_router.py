from core.runtime.runtime_decision_router import RuntimeDecisionRouter


def test_runtime_decision_router():

    router = RuntimeDecisionRouter()

    result = router.route_decision(
        "expand"
    )

    assert result["status"] == "decision_routed"