from core.runtime.runtime_response_formatter import RuntimeResponseFormatter


def test_runtime_response_formatter():
    formatter = RuntimeResponseFormatter()

    result = formatter.format({
        "status": "success",
        "execution": [1, 2],
        "plan": ["a", "b"]
    })

    assert result["completed_tasks"] == 2