from core.runtime.runtime_learning_engine import RuntimeLearningEngine


def test_runtime_learning_engine():

    engine = (
        RuntimeLearningEngine()
    )

    engine.record(
        "errors",
        "sandbox failure"
    )

    summary = engine.summarize()

    assert summary["errors"]["count"] == 1