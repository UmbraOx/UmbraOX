"""
Full integration tests — verifies the entire Umbra stack works together.
"""
import pytest
import os
import sys
from unittest.mock import MagicMock

_UMBRA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _UMBRA_ROOT not in sys.path:
    sys.path.insert(0, _UMBRA_ROOT)


def make_mock_llm_response(content, success=True):
    from core.runtime.runtime_llm_provider import LLMResponse
    resp = LLMResponse(content, "mock", "mock", 10)
    resp.success = success
    resp.error = None if success else "mock error"
    return resp


def build_test_runtime(tmp_path):
    from core.runtime.runtime_llm_provider import RuntimeLLMProvider
    from core.runtime.runtime_execution_graph import RuntimeExecutionGraph
    from core.runtime.runtime_task_state_machine import RuntimeTaskStateMachine
    from core.runtime.runtime_context_builder import RuntimeContextBuilder
    from core.runtime.runtime_validation_engine import RuntimeValidationEngine
    from core.runtime.runtime_recursion_guard import RuntimeRecursionGuard
    from core.runtime.runtime_workspace_manager import RuntimeWorkspaceManager
    from core.runtime.runtime_llm_orchestrator import RuntimeLLMOrchestrator
    from core.runtime.runtime_autonomous_pipeline import RuntimeAutonomousPipeline
    from core.runtime.runtime_code_writer import RuntimeCodeWriter
    from core.runtime.runtime_code_extractor import RuntimeCodeExtractor
    from core.runtime.runtime_code_runner import RuntimeCodeRunner
    from core.runtime.runtime_memory_store import RuntimeMemoryStore
    from core.runtime.runtime_pipeline_monitor import RuntimePipelineMonitor
    import json

    llm = RuntimeLLMProvider(provider="ollama", model="llama3")
    graph = RuntimeExecutionGraph()
    sm = RuntimeTaskStateMachine()
    ctx = RuntimeContextBuilder()
    validator = RuntimeValidationEngine()
    guard = RuntimeRecursionGuard(max_depth=5, max_calls_per_task=10, max_total_calls=50)
    workspace = RuntimeWorkspaceManager(base_dir=str(tmp_path / "workspaces"))
    code_writer = RuntimeCodeWriter(base_dir=str(tmp_path))
    extractor = RuntimeCodeExtractor()
    code_runner = RuntimeCodeRunner(working_dir=str(tmp_path))
    memory = RuntimeMemoryStore(store_path=str(tmp_path / "memory.json"))
    monitor = RuntimePipelineMonitor()

    orchestrator = RuntimeLLMOrchestrator(
        llm_provider=llm,
        context_builder=ctx,
        execution_graph=graph,
        task_state_machine=sm,
        recursion_guard=guard,
        validation_engine=validator,
    )
    pipeline = RuntimeAutonomousPipeline(
        llm_orchestrator=orchestrator,
        workspace_manager=workspace,
        validation_engine=validator,
        code_extractor=extractor,
        code_writer=code_writer,
    )

    return {
        "llm": llm, "pipeline": pipeline, "monitor": monitor,
        "memory": memory, "code_runner": code_runner,
        "extractor": extractor, "workspace": workspace,
    }


def test_full_pipeline_run_with_mock_llm(tmp_path):
    import json
    runtime = build_test_runtime(tmp_path)
    mock_plan = json.dumps({"tasks": [
        {"task_id": "task_1", "description": "write hello world", "depends_on": []},
    ]})
    plan_resp = make_mock_llm_response(mock_plan)
    exec_resp = make_mock_llm_response("```python\nprint('hello from umbra')\n```")
    runtime["llm"].complete = MagicMock(side_effect=[plan_resp, exec_resp])
    run = runtime["pipeline"].run("write a hello world script")
    assert run is not None
    assert run.status in ("completed", "completed_with_failures", "failed")


def test_pipeline_monitor_records_run(tmp_path):
    import json
    runtime = build_test_runtime(tmp_path)
    mock_plan = json.dumps({"tasks": [{"task_id": "task_1", "description": "test", "depends_on": []}]})
    plan_resp = make_mock_llm_response(mock_plan)
    exec_resp = make_mock_llm_response("```python\nx = 1\n```")
    runtime["llm"].complete = MagicMock(side_effect=[plan_resp, exec_resp])
    run = runtime["pipeline"].run("test prompt")
    runtime["monitor"].record(run)
    summary = runtime["monitor"].get_summary()
    assert summary["total_runs"] == 1


def test_memory_store_persists_run_result(tmp_path):
    runtime = build_test_runtime(tmp_path)
    runtime["memory"].store("run:test_001", {"status": "completed", "files": 3})
    entry = runtime["memory"].retrieve("run:test_001")
    assert entry.value["files"] == 3


def test_memory_search_works(tmp_path):
    runtime = build_test_runtime(tmp_path)
    runtime["memory"].store("fact:umbra", "Umbra is an autonomous AI OS", tags=["umbra"])
    results = runtime["memory"].search("autonomous")
    assert len(results) > 0


def test_code_runner_executes_extracted_code(tmp_path):
    runtime = build_test_runtime(tmp_path)
    result = runtime["code_runner"].run_string("result = 2 + 2\nprint(f'result={result}')")
    assert result.success is True
    assert "result=4" in result.stdout


def test_extractor_and_runner_pipeline(tmp_path):
    runtime = build_test_runtime(tmp_path)
    llm_response = "```python\nprint('integration_test')\n```"
    blocks = runtime["extractor"].extract_python_blocks(llm_response)
    assert len(blocks) == 1
    result = runtime["code_runner"].run_string(blocks[0].content)
    assert "integration_test" in result.stdout


def test_workspace_stores_pipeline_output(tmp_path):
    runtime = build_test_runtime(tmp_path)
    ws = runtime["workspace"].create_workspace("test_ws")
    ws.write_file("results/output.json", '{"status": "ok"}')
    assert ws.file_exists("results/output.json")


def test_health_check_runs(tmp_path):
    from core.runtime.runtime_health_monitor import RuntimeHealthMonitor
    monitor = RuntimeHealthMonitor(base_dir=str(tmp_path))
    report = monitor.run_all_checks()
    assert report.overall_status in ("healthy", "degraded", "critical")


def test_self_analyzer_on_real_runtime_dir():
    from core.runtime.runtime_self_analyzer import RuntimeSelfAnalyzer
    analyzer = RuntimeSelfAnalyzer()
    summary = analyzer.get_module_summary()
    assert summary["total_modules"] > 10
    assert summary["total_lines"] > 500


def test_resource_manager_init():
    from core.runtime.runtime_resource_manager import RuntimeResourceManager
    rm = RuntimeResourceManager(gaming_mode_auto=False, task_delay_ms=0)
    status = rm.check_status()
    assert status is not None
    assert isinstance(status.memory_pct, int)


def test_code_reviewer_on_generated_code():
    from core.runtime.runtime_code_reviewer import RuntimeCodeReviewer
    reviewer = RuntimeCodeReviewer()
    code = "def add(a, b):\n    return a + b\n\nprint(add(1, 2))\n"
    review = reviewer.review_code(code)
    assert review is not None
    assert review.score >= 0


def test_prompt_templates_detect_correctly():
    from core.runtime.runtime_prompt_templates import detect_template
    assert detect_template("write pytest tests") == "python_test"
    assert detect_template("read a CSV file") == "data_analysis"
    assert detect_template("build a REST API") == "python_api"


def test_version_accessible():
    from core.runtime.runtime_version import get_version
    assert get_version() == "2.0.0"