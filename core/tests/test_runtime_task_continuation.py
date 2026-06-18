import pytest
from unittest.mock import MagicMock
from core.runtime.runtime_task_continuation import RuntimeTaskContinuation, ContinuationRecord
from core.runtime.runtime_autonomous_pipeline import PipelineRun
from core.runtime.runtime_llm_orchestrator import OrchestrationResult


def make_failed_run(run_id="run_0001", prompt="build an app"):
    run = PipelineRun(run_id, prompt)
    run.status = "completed_with_failures"

    success_result = OrchestrationResult(True, f"{run_id}_task_1", "done", "ctx")
    fail_result = OrchestrationResult(False, f"{run_id}_task_2", "", "", metadata={"error": "LLM timeout"})

    run.results = [success_result, fail_result]
    return run


def make_complete_run(run_id="run_0002", prompt="another task"):
    run = PipelineRun(run_id, prompt)
    run.status = "completed"
    run.results = [OrchestrationResult(True, f"{run_id}_task_1", "success", "ctx")]
    return run


@pytest.fixture
def continuation(tmp_path):
    return RuntimeTaskContinuation(continuations_dir=str(tmp_path))


def test_save_from_failed_run(continuation):
    run = make_failed_run()
    record = continuation.save_from_pipeline_run(run)
    assert record is not None
    assert record.continuation_id == "cont_run_0001"


def test_save_returns_none_for_complete_run(continuation):
    run = make_complete_run()
    record = continuation.save_from_pipeline_run(run)
    assert record is None


def test_load_saved_continuation(continuation):
    run = make_failed_run()
    continuation.save_from_pipeline_run(run)
    loaded = continuation.load("cont_run_0001")
    assert loaded is not None
    assert loaded.original_prompt == "build an app"


def test_remaining_tasks_count(continuation):
    run = make_failed_run()
    record = continuation.save_from_pipeline_run(run)
    assert len(record.remaining_tasks) == 1


def test_completed_tasks_recorded(continuation):
    run = make_failed_run()
    record = continuation.save_from_pipeline_run(run)
    assert len(record.completed_tasks) == 1


def test_list_continuations(continuation):
    run1 = make_failed_run("run_001", "task one")
    run2 = make_failed_run("run_002", "task two")
    continuation.save_from_pipeline_run(run1)
    continuation.save_from_pipeline_run(run2)
    listed = continuation.list_continuations()
    assert len(listed) == 2


def test_delete_continuation(continuation):
    run = make_failed_run()
    continuation.save_from_pipeline_run(run)
    result = continuation.delete("cont_run_0001")
    assert result is True
    assert continuation.load("cont_run_0001") is None


def test_get_pending_count(continuation):
    run = make_failed_run()
    continuation.save_from_pipeline_run(run)
    count = continuation.get_pending_count("cont_run_0001")
    assert count == 1


def test_has_pending_true(continuation):
    run = make_failed_run()
    continuation.save_from_pipeline_run(run)
    assert continuation.has_pending() is True


def test_has_pending_false(continuation):
    assert continuation.has_pending() is False


def test_continuation_record_to_dict():
    rec = ContinuationRecord("c1", "build app", [{"task_id": "t1"}])
    d = rec.to_dict()
    assert d["continuation_id"] == "c1"
    assert len(d["remaining_tasks"]) == 1


def test_continuation_from_dict():
    data = {
        "continuation_id": "c2",
        "original_prompt": "test",
        "remaining_tasks": [],
        "completed_tasks": [],
        "created_at": "2025-01-01",
        "resumed_count": 2,
    }
    rec = ContinuationRecord.from_dict(data)
    assert rec.resumed_count == 2


def test_get_all_pending(continuation):
    run1 = make_failed_run("r1", "p1")
    run2 = make_failed_run("r2", "p2")
    continuation.save_from_pipeline_run(run1)
    continuation.save_from_pipeline_run(run2)
    pending = continuation.get_all_pending()
    assert len(pending) == 2