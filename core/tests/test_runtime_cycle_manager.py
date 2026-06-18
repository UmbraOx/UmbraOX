from core.runtime.runtime_cycle_manager import RuntimeCycleManager


def test_runtime_cycle_manager():

    manager = RuntimeCycleManager()

    result = manager.run_cycle()

    assert result["cycle"] == "completed"