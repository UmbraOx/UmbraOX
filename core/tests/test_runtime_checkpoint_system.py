from core.runtime.runtime_checkpoint_system import (
    RuntimeCheckpointSystem,
)


def test_runtime_checkpoint_system():
    system = RuntimeCheckpointSystem()

    state = {
        "tasks": [1, 2, 3]
    }

    system.create_checkpoint(
        "alpha",
        state,
    )

    state["tasks"].append(4)

    restored = system.restore_checkpoint(
        "alpha"
    )

    assert restored["tasks"] == [1, 2, 3]