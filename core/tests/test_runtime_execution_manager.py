from core.runtime.runtime_execution_manager import (
    RuntimeExecutionManager
)


def successful_executor(
    objective
):

    return {
        "objective": objective,
        "status": "done"
    }


def test_runtime_execution_manager():

    manager = (
        RuntimeExecutionManager()
    )

    result = manager.execute(
        "test objective",
        successful_executor
    )

    assert result["success"] is True

    assert (
        result["context"]["status"]
        == "completed"
    )