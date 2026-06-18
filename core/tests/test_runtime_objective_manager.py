from core.runtime.runtime_objective_manager import RuntimeObjectiveManager


def test_runtime_objective_manager():

    manager = RuntimeObjectiveManager()

    result = manager.create_objective(
        "improve runtime"
    )

    assert result["status"] == "objective_created"