from core.runtime.runtime_integrity_monitor import RuntimeIntegrityMonitor


def test_runtime_integrity_monitor():
    monitor = RuntimeIntegrityMonitor()

    result = monitor.run_integrity_check()

    assert result["healthy"] is True