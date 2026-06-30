import pytest
from core.runtime.runtime_pipeline_monitor import RuntimePipelineMonitor, PipelineMetrics
from core.runtime.runtime_autonomous_pipeline import PipelineRun


def make_run(status="completed", tasks=3, files=1, error=None):
    run = PipelineRun("run_test", "test prompt")
    run.status = status
    run.tasks = [{"task_id": f"t{i}"} for i in range(tasks)]
    run.written_files = [{"file": f"f{i}.py", "lines": 10} for i in range(files)]
    run.error = error
    from datetime import datetime, timedelta
    run.started_at = datetime.now().isoformat()
    run.completed_at = (datetime.now() + timedelta(seconds=2)).isoformat()
    return run


def test_record_run(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    run = make_run()
    monitor.record(run)
    assert monitor.metrics.total_runs == 1


def test_success_rate_100(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run("completed"))
    monitor.record(make_run("completed"))
    assert monitor.metrics.success_rate() == 100.0


def test_success_rate_50(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run("completed"))
    monitor.record(make_run("failed"))
    assert monitor.metrics.success_rate() == 50.0


def test_total_files_tracked(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run(files=3))
    monitor.record(make_run(files=2))
    assert monitor.metrics.total_files_written == 5


def test_total_tasks_tracked(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run(tasks=4))
    monitor.record(make_run(tasks=2))
    assert monitor.metrics.total_tasks_executed == 6


def test_get_summary(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run())
    summary = monitor.get_summary()
    assert "total_runs" in summary
    assert "success_rate_pct" in summary
    assert "total_files_written" in summary


def test_get_recent_runs(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    for i in range(5):
        monitor.record(make_run())
    recent = monitor.get_recent_runs(3)
    assert len(recent) == 3


def test_failure_patterns(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run("failed", error="LLM timeout"))
    monitor.record(make_run("failed", error="LLM timeout"))
    patterns = monitor.get_failure_patterns()
    assert any("LLM timeout" in k for k in patterns)


def test_reset(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run())
    monitor.reset()
    assert monitor.metrics.total_runs == 0
    assert len(monitor.run_log) == 0


def test_avg_duration(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run())
    assert monitor.metrics.avg_duration() >= 0


def test_metrics_to_dict(make_run=make_run):
    monitor = RuntimePipelineMonitor()
    monitor.record(make_run())
    d = monitor.metrics.to_dict()
    assert "total_runs" in d
    assert "avg_duration_seconds" in d