from core.runtime.runtime_state_manager import RuntimeStateManager


def test_runtime_state_manager():

    manager = RuntimeStateManager()

    manager.set(
        "mode",
        "active"
    )

    assert manager.get("mode") == "active"