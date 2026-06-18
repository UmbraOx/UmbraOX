from core.runtime.runtime_decision_engine import RuntimeDecisionEngine


def test_runtime_decision_engine():

    engine = (
        RuntimeDecisionEngine()
    )

    choice = engine.choose(
        [
            {
                "safe": True,
                "efficient": True,
                "autonomous": True
            },
            {
                "safe": False,
                "efficient": False,
                "autonomous": False
            }
        ]
    )

    assert choice["safe"] is True