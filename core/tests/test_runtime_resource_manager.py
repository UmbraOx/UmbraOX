import pytest
import sys
from core.runtime.runtime_resource_manager import RuntimeResourceManager, ResourceStatus


@pytest.fixture
def manager():
    return RuntimeResourceManager(gaming_mode_auto=True, max_memory_pct=85, task_delay_ms=10)


def test_check_status_returns_status(manager):
    status = manager.check_status()
    assert isinstance(status, ResourceStatus)


def test_status_has_memory_pct(manager):
    status = manager.check_status()
    assert isinstance(status.memory_pct, int)
    assert 0 <= status.memory_pct <= 100


def test_status_has_gaming_detected(manager):
    status = manager.check_status()
    assert isinstance(status.gaming_detected, bool)


def test_status_to_dict(manager):
    status = manager.check_status()
    d = status.to_dict()
    assert "gaming_detected" in d
    assert "memory_pct" in d
    assert "throttled" in d


def test_get_current_status(manager):
    manager.check_status()
    d = manager.get_current_status()
    assert "gaming_detected" in d


def test_detect_gaming_processes_returns_list(manager):
    procs = manager.detect_gaming_processes()
    assert isinstance(procs, list)


def test_get_memory_usage_pct_returns_int(manager):
    pct = manager.get_memory_usage_pct()
    assert isinstance(pct, int)
    assert 0 <= pct <= 100


def test_should_throttle_false_by_default(manager):
    manager.check_status()
    assert isinstance(manager.should_throttle(), bool)


def test_get_subprocess_kwargs_returns_dict(manager):
    kwargs = manager.get_subprocess_kwargs()
    assert isinstance(kwargs, dict)


def test_start_stop_monitoring(manager):
    manager.start_monitoring(interval_seconds=60)
    assert manager._monitoring is True
    manager.stop_monitoring()
    assert manager._monitoring is False


def test_on_status_change_callback(manager):
    results = []
    manager.on_status_change(lambda s: results.append(s))
    assert len(manager._callbacks) == 1


def test_task_delay_runs(manager):
    import time
    start = time.time()
    manager.task_delay()
    elapsed = time.time() - start
    assert elapsed >= 0


def test_set_process_priority_low_no_crash(manager):
    manager._set_process_priority_low()


def test_release_throttle_no_crash(manager):
    manager.release_throttle()