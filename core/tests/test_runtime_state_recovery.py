from core.runtime.runtime_state_recovery import RuntimeStateRecovery


def test_runtime_state_recovery():
    recovery = RuntimeStateRecovery()

    recovery.save_state({"online": True})

    state = recovery.recover_state()

    assert state["online"] is True