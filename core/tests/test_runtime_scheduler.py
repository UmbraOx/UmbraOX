import pytest
import time
from core.runtime.runtime_scheduler import RuntimeScheduler, ScheduledJob


@pytest.fixture
def scheduler():
    return RuntimeScheduler(check_interval=1)


def test_add_job(scheduler):
    scheduler.add_job("test_job", lambda: None, interval_seconds=60)
    assert len(scheduler.jobs) == 1


def test_job_runs_when_due(scheduler):
    results = []
    scheduler.add_job("collect", lambda: results.append(1), interval_seconds=0)
    scheduler.jobs[0].run()
    assert len(results) == 1


def test_job_not_due_before_interval(scheduler):
    job = scheduler.add_job("timed", lambda: None, interval_seconds=3600)
    job.last_run = time.time()
    assert job.is_due() is False


def test_job_due_when_no_last_run(scheduler):
    job = scheduler.add_job("fresh", lambda: None, interval_seconds=60)
    assert job.is_due() is True


def test_job_run_count_increments(scheduler):
    job = scheduler.add_job("counter", lambda: None, interval_seconds=0)
    job.run()
    job.run()
    assert job.run_count == 2


def test_job_records_error(scheduler):
    def bad_fn():
        raise ValueError("test error")
    job = scheduler.add_job("bad", bad_fn, interval_seconds=0)
    result = job.run()
    assert result is False
    assert len(job.errors) == 1


def test_run_now(scheduler):
    results = []
    scheduler.add_job("immediate", lambda: results.append(True), interval_seconds=9999)
    scheduler.run_now("immediate")
    assert len(results) == 1


def test_run_now_missing_job(scheduler):
    result = scheduler.run_now("nonexistent_job")
    assert result is False


def test_enable_disable_job(scheduler):
    job = scheduler.add_job("toggle", lambda: None, interval_seconds=0)
    scheduler.disable_job("toggle")
    assert job.enabled is False
    assert job.is_due() is False
    scheduler.enable_job("toggle")
    assert job.enabled is True


def test_get_status(scheduler):
    scheduler.add_job("status_test", lambda: None, interval_seconds=60)
    status = scheduler.get_status()
    assert len(status) == 1
    assert "name" in status[0]
    assert "run_count" in status[0]


def test_job_to_dict():
    job = ScheduledJob("test", lambda: None, 300, True)
    d = job.to_dict()
    assert d["name"] == "test"
    assert d["interval_seconds"] == 300
    assert d["enabled"] is True


def test_scheduler_start_stop(scheduler):
    scheduler.add_job("bg", lambda: None, interval_seconds=9999)
    scheduler.start()
    assert scheduler._running is True
    scheduler.stop()
    assert scheduler._running is False