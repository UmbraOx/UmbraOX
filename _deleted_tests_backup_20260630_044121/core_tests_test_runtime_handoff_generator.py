import pytest
import os
import json
from core.runtime.runtime_handoff_generator import RuntimeHandoffGenerator
from unittest.mock import MagicMock


def make_generator(tmp_path):
    return RuntimeHandoffGenerator(base_dir=str(tmp_path))


def make_mock_runtime(tmp_path):
    from core.runtime.runtime_llm_provider import RuntimeLLMProvider
    from core.runtime.runtime_execution_graph import RuntimeExecutionGraph
    from core.runtime.runtime_task_state_machine import RuntimeTaskStateMachine
    from core.runtime.runtime_autonomous_pipeline import RuntimeAutonomousPipeline
    from core.runtime.runtime_workspace_manager import RuntimeWorkspaceManager
    from core.runtime.runtime_validation_engine import RuntimeValidationEngine
    from core.runtime.runtime_context_builder import RuntimeContextBuilder
    from core.runtime.runtime_llm_orchestrator import RuntimeLLMOrchestrator

    llm = MagicMock()
    llm.get_provider.return_value = "ollama"
    llm.get_model.return_value = "llama3"
    llm.is_configured.return_value = True

    graph = RuntimeExecutionGraph()
    sm = RuntimeTaskStateMachine()

    return {
        "llm": llm,
        "graph": graph,
        "state_machine": sm,
        "pipeline": MagicMock(get_run_history=lambda: []),
    }


def test_generate_creates_json_file(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    path, handoff = gen.generate(runtime)
    assert os.path.exists(path)
    assert path.endswith(".json")


def test_generate_handoff_has_required_keys(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    _, handoff = gen.generate(runtime)
    assert "generated_at" in handoff
    assert "llm_provider" in handoff
    assert "session_stats" in handoff
    assert "next_steps" in handoff


def test_generate_markdown_creates_file(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    path, md = gen.generate_markdown(runtime)
    assert os.path.exists(path)
    assert path.endswith(".md")
    assert "UMBRA HANDOFF" in md


def test_markdown_contains_provider(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    _, md = gen.generate_markdown(runtime)
    assert "ollama" in md


def test_handoff_json_is_valid(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    path, _ = gen.generate(runtime)
    with open(path) as f:
        data = json.load(f)
    assert data["llm_provider"] == "ollama"


def test_next_steps_with_no_runs(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    _, handoff = gen.generate(runtime)
    assert len(handoff["next_steps"]) > 0


def test_session_stats_structure(tmp_path):
    gen = make_generator(tmp_path)
    runtime = make_mock_runtime(tmp_path)
    _, handoff = gen.generate(runtime)
    stats = handoff["session_stats"]
    assert "total_runs" in stats
    assert "graph_nodes" in stats


def test_generate_snapshot_manager_fixed(tmp_path):
    from core.runtime.runtime_snapshot_manager import RuntimeSnapshotManager
    sm = RuntimeSnapshotManager(snapshot_dir=str(tmp_path / "snapshots"))
    path = sm.create_snapshot({"test": "data"}, label="test")
    assert os.path.exists(path)
    restored = sm.restore_snapshot(path)
    assert restored["runtime_state"]["test"] == "data"