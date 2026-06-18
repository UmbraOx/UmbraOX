import pytest
import sys
import os
from unittest.mock import MagicMock, patch
import json

_UMBRA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _UMBRA_ROOT not in sys.path:
    sys.path.insert(0, _UMBRA_ROOT)


def test_build_runtime_returns_dict():
    from umbra import build_runtime
    runtime = build_runtime()
    required = [
        "llm", "pipeline", "graph", "code_writer", "extractor",
        "sessions", "continuation", "code_runner", "config",
        "monitor", "memory", "health", "run_validator",
        "reviewer", "replayer", "conversation", "game_tester",
    ]
    for key in required:
        assert key in runtime, f"Missing: {key}"


def test_runtime_pipeline_functional():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["pipeline"], "run")


def test_llm_provider_present():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["llm"], "complete")


def test_print_config_runs(capsys):
    from umbra import print_config
    print_config()
    out = capsys.readouterr().out
    # Test that config output contains expected content (updated for new format)
    assert "UMBRA CONFIG" in out or "LLM" in out or "Ollama" in out


def test_print_status_runs(capsys):
    from umbra import build_runtime, print_status
    runtime = build_runtime()
    print_status(runtime)
    out = capsys.readouterr().out
    assert "Provider" in out


def test_run_prompt_uses_pipeline():
    from umbra import build_runtime, run_prompt
    from core.runtime.runtime_llm_provider import LLMResponse
    from unittest.mock import patch

    runtime = build_runtime()

    mock_plan = json.dumps({"tasks": [
        {"task_id": "task_1", "description": "analyze", "depends_on": []},
    ]})
    plan_resp = LLMResponse(mock_plan, "mock", "mock", 10)
    plan_resp.success = True
    plan_resp.error = None
    exec_resp = LLMResponse("```python\nprint('hello')\n```", "mock", "mock", 10)
    exec_resp.success = True
    exec_resp.error = None

    runtime["llm"].complete = MagicMock(side_effect=[plan_resp, exec_resp, exec_resp])

    # Mock direct generator to be unavailable so pipeline is used
    runtime["direct_generator"].is_available = MagicMock(return_value=False)

    run = run_prompt(runtime, "write a python script that prints hello world")
    assert run is not None
    assert run.run_id is not None


def test_extractor_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    blocks = runtime["extractor"].extract_python_blocks("```python\nx = 1\n```")
    assert len(blocks) == 1


def test_session_manager_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["sessions"], "create_session")


def test_code_runner_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    result = runtime["code_runner"].run_string("print('umbra_test')")
    assert result.success is True
    assert "umbra_test" in result.stdout


def test_config_manager_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert runtime["config"].get("llm_provider") is not None


def test_memory_store_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    runtime["memory"].store("test_key_umbra", "test_value")
    entry = runtime["memory"].retrieve("test_key_umbra")
    assert entry is not None


def test_pipeline_monitor_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["monitor"], "record")


def test_health_monitor_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["health"], "run_all_checks")


def test_print_metrics_runs(capsys):
    from umbra import build_runtime, print_metrics
    runtime = build_runtime()
    print_metrics(runtime)
    out = capsys.readouterr().out
    assert "PIPELINE METRICS" in out or "Total" in out or "runs" in out.lower()


def test_reviewer_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["reviewer"], "review_code")


def test_replayer_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["replayer"], "list_replayable_sessions")


def test_run_validator_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    assert hasattr(runtime["run_validator"], "validate_run")


def test_scheduler_starts():
    from umbra import build_runtime
    runtime = build_runtime()
    sched = runtime.get("scheduler")
    if sched:
        assert sched._running is True
        assert len(sched.jobs) > 0


def test_conversation_engine_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    conv = runtime.get("conversation")
    assert conv is not None
    assert hasattr(conv, "classify")
    assert hasattr(conv, "answer_question")


def test_game_tester_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    tester = runtime.get("game_tester")
    assert tester is not None
    assert hasattr(tester, "test_file")


def test_image_generator_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    img = runtime.get("image_generator")
    assert img is not None
    assert hasattr(img, "generate")
    assert hasattr(img, "is_available")


def test_voice_input_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    voice = runtime.get("voice_input")
    assert voice is not None
    assert hasattr(voice, "is_available")

def test_direct_generator_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    dg = runtime.get("direct_generator")
    assert dg is not None
    assert hasattr(dg, "generate")
    assert hasattr(dg, "is_available")


def test_project_manager_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    pm = runtime.get("project_manager")
    assert pm is not None
    p = pm.create_project("TestProjectXYZ", "test")
    assert p.name == "TestProjectXYZ"
    assert p.slug == "testprojectxyz"


def test_studio_agents_in_runtime():
    from umbra import build_runtime
    runtime = build_runtime()
    agents = runtime.get("studio_agents")
    assert agents is not None
    agent_list = agents.list_agents()
    assert len(agent_list) >= 5