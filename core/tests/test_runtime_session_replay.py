import pytest
import os
import json
from unittest.mock import MagicMock
from core.runtime.runtime_session_replay import RuntimeSessionReplay, SessionReplay
from core.runtime.runtime_autonomous_pipeline import PipelineRun


def make_session_file(tmp_path, session_id, runs):
    data = {
        "session_id": session_id,
        "created_at": "2026-05-25T10:00:00",
        "runs": runs,
    }
    path = tmp_path / f"session_{session_id}.json"
    path.write_text(json.dumps(data))
    return path


def make_mock_pipeline(status="completed", files=2):
    pipeline = MagicMock()
    run = PipelineRun("run_replay_001", "test prompt")
    run.status = status
    run.written_files = [{"file": f"code/f{i}.py", "lines": 10} for i in range(files)]
    pipeline.run.return_value = run
    return pipeline


def test_list_replayable_sessions(tmp_path):
    make_session_file(tmp_path, "abc123", [{"run_id": "r1", "prompt": "build x", "status": "completed", "written_files": []}])
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    sessions = replay.list_replayable_sessions()
    assert len(sessions) == 1
    assert sessions[0]["session_id"] == "abc123"


def test_load_session(tmp_path):
    make_session_file(tmp_path, "sess1", [])
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    data = replay.load_session("sess1")
    assert data is not None
    assert data["session_id"] == "sess1"


def test_load_missing_session(tmp_path):
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    result = replay.load_session("nonexistent")
    assert result is None


def test_extract_prompts(tmp_path):
    runs = [
        {"run_id": "r1", "prompt": "build a script", "status": "completed", "written_files": []},
        {"run_id": "r2", "prompt": "write tests", "status": "completed", "written_files": []},
    ]
    make_session_file(tmp_path, "s1", runs)
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    data = replay.load_session("s1")
    prompts = replay.extract_prompts(data)
    assert len(prompts) == 2
    assert prompts[0]["prompt"] == "build a script"


def test_replay_session_dry_run(tmp_path):
    runs = [{"run_id": "r1", "prompt": "build something", "status": "completed", "written_files": []}]
    make_session_file(tmp_path, "s_dry", runs)
    pipeline = make_mock_pipeline()
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    result = replay.replay_session("s_dry", pipeline, dry_run=True)
    assert result is not None
    assert result.runs[0]["status"] == "dry_run_skipped"
    assert not pipeline.run.called


def test_replay_session_executes(tmp_path):
    runs = [{"run_id": "r1", "prompt": "build something", "status": "completed", "written_files": []}]
    make_session_file(tmp_path, "s_exec", runs)
    pipeline = make_mock_pipeline()
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    result = replay.replay_session("s_exec", pipeline, dry_run=False)
    assert pipeline.run.called
    assert result.runs[0]["replayed"] is True


def test_replay_history_recorded(tmp_path):
    runs = [{"run_id": "r1", "prompt": "task", "status": "completed", "written_files": []}]
    make_session_file(tmp_path, "s_hist", runs)
    pipeline = make_mock_pipeline()
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    replay.replay_session("s_hist", pipeline, dry_run=True)
    assert len(replay.get_replay_history()) == 1


def test_session_replay_to_dict():
    replay = SessionReplay("sess_001", [{"prompt": "test"}], {"dry_run": True})
    d = replay.to_dict()
    assert d["session_id"] == "sess_001"
    assert d["total_runs"] == 1


def test_missing_session_replay_returns_none(tmp_path):
    pipeline = make_mock_pipeline()
    replay = RuntimeSessionReplay(sessions_dir=str(tmp_path))
    result = replay.replay_session("nonexistent_session", pipeline)
    assert result is None