from core.runtime.runtime_autonomous_executor import RuntimeAutonomousExecutor


def test_runtime_autonomous_executor():
    executor = RuntimeAutonomousExecutor()

    result = executor.execute_plan({
        "goal": "Test",
        "tasks": ["task1", "task2"],
    })

    assert result["success"] is True