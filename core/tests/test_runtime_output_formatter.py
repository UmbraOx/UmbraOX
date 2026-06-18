import pytest
from core.runtime.runtime_output_formatter import RuntimeOutputFormatter
from core.runtime.runtime_autonomous_pipeline import PipelineRun
from core.runtime.runtime_llm_orchestrator import OrchestrationResult


def make_formatter():
    return RuntimeOutputFormatter()


def make_run(status="completed"):
    run = PipelineRun("run_0001", "build a REST API")
    run.status = status
    run.written_files = [{"file": "code/task.py", "lines": 42}]
    run.results = []
    return run


def test_format_run_contains_run_id():
    formatter = make_formatter()
    run = make_run()
    output = formatter.format_run(run)
    assert "run_0001" in output


def test_format_run_contains_status():
    formatter = make_formatter()
    run = make_run("completed")
    output = formatter.format_run(run)
    assert "completed" in output


def test_format_run_contains_prompt():
    formatter = make_formatter()
    run = make_run()
    output = formatter.format_run(run)
    assert "build a REST API" in output


def test_format_run_shows_files():
    formatter = make_formatter()
    run = make_run()
    output = formatter.format_run(run)
    assert "FILES WRITTEN" in output
    assert "42 lines" in output


def test_format_run_with_error():
    formatter = make_formatter()
    run = make_run("failed")
    run.error = "pipeline crashed"
    output = formatter.format_run(run)
    assert "pipeline crashed" in output


def test_format_result_success():
    formatter = make_formatter()
    result = OrchestrationResult(True, "task_1", "great output", "context")
    output = formatter.format_result(result)
    assert "[OK]" in output
    assert "task_1" in output


def test_format_result_failure():
    formatter = make_formatter()
    result = OrchestrationResult(False, "task_2", "", "", metadata={"error": "timeout"})
    output = formatter.format_result(result)
    assert "[FAIL]" in output
    assert "timeout" in output


def test_format_graph_summary():
    formatter = make_formatter()
    summary = {
        "total": 5,
        "complete": True,
        "has_failures": False,
        "by_state": {"completed": 5},
    }
    output = formatter.format_graph_summary(summary)
    assert "GRAPH SUMMARY" in output
    assert "5" in output


def test_format_health_report():
    from core.runtime.runtime_health_monitor import HealthReport
    formatter = make_formatter()
    report = HealthReport()
    report.add_check("test_check", "pass", "all good")
    output = formatter.format_health_report(report)
    assert "HEALTH" in output
    assert "test_check" in output


def test_format_session_history_empty():
    formatter = make_formatter()
    output = formatter.format_session_history([])
    assert "No runs" in output


def test_format_session_history_with_runs():
    formatter = make_formatter()
    runs = [
        {"run_id": "run_0001", "status": "completed", "written_files": [], "prompt": "test prompt"},
    ]
    output = formatter.format_session_history(runs)
    assert "run_0001" in output
    assert "completed" in output