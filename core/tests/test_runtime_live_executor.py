from core.runtime.runtime_live_executor import RuntimeLiveExecutor


def test_runtime_live_executor():

    executor = RuntimeLiveExecutor()

    result = executor.execute(
        "test_task"
    )

    assert result["status"] == "executed"