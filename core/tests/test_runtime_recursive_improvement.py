from core.runtime.runtime_recursive_improvement import RuntimeRecursiveImprovement


def test_runtime_recursive_improvement():

    engine = (
        RuntimeRecursiveImprovement()
    )

    result = engine.improve(
        {
            "issues": [
                "memory pressure",
                "retry overflow"
            ]
        }
    )

    assert result["success"] is True
    assert result["issues_processed"] == 2