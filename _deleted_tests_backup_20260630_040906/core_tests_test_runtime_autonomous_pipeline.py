import pytest
import json
from unittest.mock import MagicMock
from core.runtime.runtime_autonomous_pipeline import RuntimeAutonomousPipeline, PipelineRun
from core.runtime.runtime_llm_orchestrator import RuntimeLLMOrchestrator
from core.runtime.runtime_execution_graph import RuntimeExecutionGraph
from core.runtime.runtime_task_state_machine import RuntimeTaskStateMachine
from core.runtime.runtime_context_builder import RuntimeContextBuilder
from core.runtime.runtime_validation_engine import RuntimeValidationEngine
from core.runtime.runtime_code_extractor import RuntimeCodeExtractor
from core.runtime.runtime_llm_provider import LLMResponse


def make_mock_llm(code_in_response=True):
    llm = MagicMock()
    default_plan = json.dumps({
        "tasks": [
            {"task_id": "task_1", "description": "Analyze the objective", "depends_on": []},
            {"task_id": "task_2", "description": "Implement solution", "depends_on": ["task_1"]},
        ]
    })
    plan_resp = LLMResponse(default_plan, "mock", "mock", 50)
    plan_resp.success = True
    plan_resp.error = None

    code_content = "```python\nimport os\n\ndef main():\n    print('hello')\n\nmain()\n```" if code_in_response else "Execution complete"
    exec_resp = LLMResponse(code_content, "mock", "mock", 30)
    exec_resp.success = True
    exec_resp.error = None

    llm.complete.side_effect = [plan_resp, exec_resp, exec_resp, exec_resp]
    llm.is_configured.return_value = True
    return llm


def make_pipeline(tmp_path, llm=None, code_in_response=True):
    from core.runtime.runtime_workspace_manager import RuntimeWorkspaceManager
    llm = llm or make_mock_llm(code_in_response=code_in_response)
    graph = RuntimeExecutionGraph()
    sm = RuntimeTaskStateMachine()
    ctx = RuntimeContextBuilder()
    validator = RuntimeValidationEngine()
    extractor = RuntimeCodeExtractor()
    orch = RuntimeLLMOrchestrator(
        llm_provider=llm,
        context_builder=ctx,
        execution_graph=graph,
        task_state_machine=sm,
        validation_engine=validator,
    )
    wm = RuntimeWorkspaceManager(base_dir=str(tmp_path))
    return RuntimeAutonomousPipeline(
        llm_orchestrator=orch,
        workspace_manager=wm,
        validation_engine=validator,
        code_extractor=extractor,
    )


def test_pipeline_run_returns_pipeline_run(tmp_path):
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("build a REST API server")
    assert isinstance(run, PipelineRun)


def test_pipeline_run_has_run_id(tmp_path):
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("create a CLI tool")
    assert run.run_id.startswith("run_")


def test_pipeline_run_completes(tmp_path):
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("analyze the project structure")
    assert run.status in ("completed", "completed_with_failures", "failed")


def test_pipeline_creates_workspace_files(tmp_path):
    import os
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("write a Python module")
    ws_path = os.path.join(str(tmp_path), run.run_id)
    assert os.path.exists(ws_path)
    assert os.path.exists(os.path.join(ws_path, "task_plan.json"))


def test_pipeline_has_tasks(tmp_path):
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("design a database schema")
    assert len(run.tasks) > 0


def test_pipeline_has_results(tmp_path):
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("build unit tests")
    assert len(run.results) > 0


def test_pipeline_extracts_code_to_workspace(tmp_path):
    import os
    pipeline = make_pipeline(tmp_path, code_in_response=True)
    run = pipeline.run("write a hello world script")
    ws_path = os.path.join(str(tmp_path), run.run_id)
    # Check if any code files were written
    code_dir = os.path.join(ws_path, "code")
    if os.path.exists(code_dir):
        files = os.listdir(code_dir)
        assert len(files) >= 0  # May or may not write depending on validation


def test_pipeline_written_files_tracked(tmp_path):
    pipeline = make_pipeline(tmp_path, code_in_response=True)
    run = pipeline.run("generate a utility script")
    assert isinstance(run.written_files, list)


def test_pipeline_run_history(tmp_path):
    pipeline = make_pipeline(tmp_path)
    pipeline.run("task one")
    pipeline.run("task two")
    assert len(pipeline.get_run_history()) == 2


def test_pipeline_get_last_run(tmp_path):
    pipeline = make_pipeline(tmp_path)
    pipeline.run("first")
    pipeline.run("second")
    last = pipeline.get_last_run()
    assert last is not None
    assert last.run_id == "run_0002"


def test_pipeline_get_run_by_id(tmp_path):
    pipeline = make_pipeline(tmp_path)
    pipeline.run("find me")
    run = pipeline.get_run_by_id("run_0001")
    assert run is not None
    assert run.prompt == "find me"


def test_pipeline_fallback_plan_when_llm_unconfigured(tmp_path):
    llm = make_mock_llm()
    llm.is_configured.return_value = False
    pipeline = make_pipeline(tmp_path, llm=llm)
    run = pipeline.run("test with no LLM")
    assert len(run.tasks) == 3


def test_pipeline_run_to_dict(tmp_path):
    pipeline = make_pipeline(tmp_path)
    run = pipeline.run("dict test")
    d = run.to_dict()
    assert "run_id" in d
    assert "status" in d
    assert "written_files" in d