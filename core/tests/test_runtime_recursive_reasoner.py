from core.runtime.runtime_recursive_reasoner import RuntimeRecursiveReasoner


def test_runtime_recursive_reasoner():

    engine = RuntimeRecursiveReasoner()

    result = engine.recursive_reason(
        "Improve runtime"
    )

    assert result["status"] == "recursive_complete"