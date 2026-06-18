from core.runtime.runtime_self_monitor import RuntimeSelfMonitor


def test_runtime_self_monitor():

    monitor = RuntimeSelfMonitor()

    result = monitor.monitor(
        "runtime_started"
    )

    assert result["status"] == "monitored"