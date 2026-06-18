from core.runtime.runtime_reasoning_engine import RuntimeReasoningEngine


def test_runtime_reasoning_engine():

    engine = RuntimeReasoningEngine()

    result = engine.reason(
        "How should Umbra improve?"
    )

    assert result["status"] == "reasoned"