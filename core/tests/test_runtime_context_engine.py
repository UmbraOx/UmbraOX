from core.runtime.runtime_context_engine import RuntimeContextEngine


def test_runtime_context_engine():

    engine = (
        RuntimeContextEngine()
    )

    engine.remember(
        "agent coordination system"
    )

    results = engine.recall(
        "coordination"
    )

    assert len(results) > 0