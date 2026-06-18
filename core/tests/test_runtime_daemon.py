import pytest
from core.runtime.runtime_daemon import RuntimeDaemon


def test_runtime_daemon():
    daemon = RuntimeDaemon()
    daemon.start()
    result = daemon.heartbeat()
    assert result["success"] is True
    assert "status" in result


def test_daemon_starts():
    daemon = RuntimeDaemon()
    daemon.start()
    assert daemon.is_running() is True


def test_daemon_stops():
    daemon = RuntimeDaemon()
    daemon.start()
    daemon.stop()
    assert daemon.is_running() is False


def test_heartbeat_when_not_running():
    daemon = RuntimeDaemon()
    result = daemon.heartbeat()
    assert result["success"] is False
    assert "error" in result


def test_heartbeat_with_no_monitor():
    daemon = RuntimeDaemon()
    daemon.start()
    result = daemon.heartbeat()
    assert result["success"] is True
    assert result["status"] == "running"


def test_heartbeat_with_mock_monitor():
    from unittest.mock import MagicMock
    monitor = MagicMock()
    monitor.quick_status.return_value = "healthy"
    daemon = RuntimeDaemon(health_monitor=monitor)
    daemon.start()
    result = daemon.heartbeat()
    assert result["status"] == "healthy"


def test_get_uptime():
    daemon = RuntimeDaemon()
    daemon.start()
    uptime = daemon.get_uptime()
    assert uptime >= 0


def test_started_at_set_on_start():
    daemon = RuntimeDaemon()
    assert daemon.started_at is None
    daemon.start()
    assert daemon.started_at is not None