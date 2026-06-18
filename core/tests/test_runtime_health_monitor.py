import pytest
from core.runtime.runtime_health_monitor import RuntimeHealthMonitor, HealthReport


@pytest.fixture
def monitor(tmp_path):
    return RuntimeHealthMonitor(base_dir=str(tmp_path))


def test_run_all_checks_returns_report(monitor):
    report = monitor.run_all_checks()
    assert isinstance(report, HealthReport)


def test_report_has_checks(monitor):
    report = monitor.run_all_checks()
    assert len(report.checks) > 0


def test_report_has_overall_status(monitor):
    report = monitor.run_all_checks()
    assert report.overall_status in ("healthy", "degraded", "critical")


def test_report_to_dict(monitor):
    report = monitor.run_all_checks()
    d = report.to_dict()
    assert "overall_status" in d
    assert "checks" in d
    assert "pass_count" in d


def test_summary_line(monitor):
    report = monitor.run_all_checks()
    line = report.summary_line()
    assert "pass=" in line


def test_check_history_recorded(monitor):
    monitor.run_all_checks()
    monitor.run_all_checks()
    assert len(monitor.get_history()) == 2


def test_add_check_pass():
    report = HealthReport()
    report.add_check("test_check", "pass", "all good")
    assert report.overall_status == "healthy"
    assert report.checks[0]["status"] == "pass"


def test_add_check_warn_degrades():
    report = HealthReport()
    report.add_check("test_check", "warn", "something off", "warn")
    assert report.overall_status == "degraded"


def test_add_check_critical_fail():
    report = HealthReport()
    report.add_check("test_check", "fail", "broken", "critical")
    assert report.overall_status == "critical"


def test_quick_status_returns_string(monitor):
    status = monitor.quick_status()
    assert isinstance(status, str)
    assert status in ("healthy", "degraded", "critical")


def test_python_version_check_passes(monitor):
    report = monitor.run_all_checks()
    python_checks = [c for c in report.checks if c["name"] == "python_version"]
    assert len(python_checks) == 1
    assert python_checks[0]["status"] in ("pass", "warn")