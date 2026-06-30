from core.runtime.runtime_task_executor import (
    RuntimeTaskExecutor,
)


def test_runtime_task_executor():
    executor = RuntimeTaskExecutor()

    result = executor.execute(
        "build_feature"
    )

    assert result["status"] == "completed"