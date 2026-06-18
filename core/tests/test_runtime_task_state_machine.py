import pytest
from core.runtime.runtime_task_state_machine import RuntimeTaskStateMachine, TaskState


def make_sm():
    sm = RuntimeTaskStateMachine()
    sm.register("task_1", {"name": "Test Task"})
    return sm


def test_register_task():
    sm = RuntimeTaskStateMachine()
    record = sm.register("task_1")
    assert record.task_id == "task_1"
    assert record.state == TaskState.PENDING


def test_register_duplicate_returns_same():
    sm = RuntimeTaskStateMachine()
    r1 = sm.register("task_1")
    r2 = sm.register("task_1")
    assert r1 is r2


def test_full_happy_path():
    sm = make_sm()
    sm.start_planning("task_1")
    sm.queue("task_1")
    sm.start_running("task_1")
    sm.start_validating("task_1")
    sm.complete("task_1", result="all good")
    assert sm.get_state("task_1") == TaskState.COMPLETED
    assert sm.get_record("task_1").result == "all good"


def test_invalid_transition_raises():
    sm = make_sm()
    with pytest.raises(ValueError):
        sm.complete("task_1")  # can't jump from PENDING to COMPLETED


def test_fail_from_running():
    sm = make_sm()
    sm.start_planning("task_1")
    sm.queue("task_1")
    sm.start_running("task_1")
    sm.fail("task_1", error="subprocess crashed")
    assert sm.get_state("task_1") == TaskState.FAILED
    assert sm.get_record("task_1").error == "subprocess crashed"


def test_retry_requeues():
    sm = make_sm()
    sm.start_planning("task_1")
    sm.queue("task_1")
    sm.start_running("task_1")
    sm.fail("task_1", error="timeout")
    sm.retry("task_1")
    assert sm.get_state("task_1") == TaskState.QUEUED
    assert sm.get_record("task_1").retry_count == 1


def test_retry_exhausted_raises():
    sm = RuntimeTaskStateMachine()
    sm.register("task_1")
    # max_retries = 3 — cycle through 3 full retries
    # After register: PENDING
    # First iteration needs full path from PENDING
    sm.start_planning("task_1")
    sm.queue("task_1")
    sm.start_running("task_1")
    sm.fail("task_1")
    sm.retry("task_1")  # retry_count=1, now QUEUED
    # Iterations 2 and 3 start from QUEUED (retry re-queues)
    for _ in range(2):
        sm.start_running("task_1")
        sm.fail("task_1")
        sm.retry("task_1")  # retry_count=2, then 3, both back to QUEUED
    # retry_count == 3 == max_retries, next retry must raise
    sm.start_running("task_1")
    sm.fail("task_1")
    with pytest.raises(RuntimeError):
        sm.retry("task_1")


def test_cancel():
    sm = make_sm()
    sm.cancel("task_1")
    assert sm.get_state("task_1") == TaskState.CANCELLED


def test_is_terminal():
    sm = make_sm()
    assert sm.is_terminal("task_1") is False
    sm.cancel("task_1")
    assert sm.is_terminal("task_1") is True


def test_get_all_by_state():
    sm = RuntimeTaskStateMachine()
    sm.register("t1")
    sm.register("t2")
    sm.register("t3")
    sm.cancel("t3")
    pending = sm.get_all_by_state(TaskState.PENDING)
    assert len(pending) == 2


def test_summary():
    sm = RuntimeTaskStateMachine()
    sm.register("t1")
    sm.register("t2")
    s = sm.summary()
    assert s["total"] == 2
    assert s["by_state"][TaskState.PENDING] == 2


def test_history_recorded():
    sm = make_sm()
    sm.start_planning("task_1")
    sm.queue("task_1")
    record = sm.get_record("task_1")
    assert len(record.history) >= 2