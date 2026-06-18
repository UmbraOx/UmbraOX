import pytest
from core.runtime.runtime_recursion_guard import RuntimeRecursionGuard, RecursionGuardError


def make_guard(**kwargs):
    return RuntimeRecursionGuard(**kwargs)


def test_normal_enter_exit():
    guard = make_guard()
    guard.enter("task_a", "step_1")
    guard.exit("task_a")
    assert guard.get_depth("task_a") == 0


def test_depth_increments():
    guard = make_guard()
    guard.enter("task_a", "step_1")
    assert guard.get_depth("task_a") == 1
    guard.enter("task_a", "step_2")
    assert guard.get_depth("task_a") == 2


def test_depth_limit_raises():
    guard = make_guard(max_depth=3)
    for i in range(3):
        guard.enter("task_a", f"step_{i}")
    with pytest.raises(RecursionGuardError, match="depth"):
        guard.enter("task_a", "step_overflow")


def test_per_task_call_limit():
    guard = make_guard(max_calls_per_task=5, max_depth=100)
    for i in range(5):
        guard.enter("task_a", f"c{i}")
        guard.exit("task_a")
    with pytest.raises(RecursionGuardError, match="call limit"):
        guard.enter("task_a", "over_limit")


def test_total_call_budget():
    guard = make_guard(max_total_calls=3, max_depth=100, max_calls_per_task=100)
    guard.enter("t1", "a")
    guard.exit("t1")
    guard.enter("t2", "b")
    guard.exit("t2")
    guard.enter("t3", "c")
    guard.exit("t3")
    with pytest.raises(RecursionGuardError, match="budget"):
        guard.enter("t4", "d")


def test_loop_detection():
    # threshold=3 means the 3rd repeat of the same fingerprint raises
    guard = RuntimeRecursionGuard(detect_loops=True, max_depth=100, max_calls_per_task=100, loop_repeat_threshold=3)
    # Enter and fully exit — fingerprint task_a:ctx:1 count = 1
    guard.enter("task_a", "ctx")
    guard.exit("task_a")
    # Second time — count = 2
    guard.enter("task_a", "ctx")
    guard.exit("task_a")
    # Third time — count = 3, should raise
    with pytest.raises(RecursionGuardError, match="loop"):
        guard.enter("task_a", "ctx")


def test_loop_detection_disabled():
    guard = make_guard(detect_loops=False, max_depth=100, max_calls_per_task=100)
    for _ in range(5):
        guard.enter("task_a", "same_context")
        guard.exit("task_a")


def test_reset_task():
    guard = make_guard(max_depth=3)
    guard.enter("task_a", "s1")
    guard.enter("task_a", "s2")
    guard.reset_task("task_a")
    assert guard.get_depth("task_a") == 0
    assert guard.get_call_count("task_a") == 0


def test_reset_all():
    guard = make_guard()
    guard.enter("task_a", "s1")
    guard.reset_all()
    assert guard.get_total_calls() == 0


def test_is_safe_returns_true():
    guard = make_guard()
    assert guard.is_safe("task_a") is True


def test_is_safe_returns_false_after_limit():
    guard = make_guard(max_calls_per_task=2, max_depth=100)
    guard.enter("task_a", "s1")
    guard.exit("task_a")
    guard.enter("task_a", "s2")
    guard.exit("task_a")
    assert guard.is_safe("task_a") is False


def test_violations_recorded():
    guard = make_guard(max_depth=1)
    guard.enter("task_a", "ok")
    try:
        guard.enter("task_a", "overflow")
    except RecursionGuardError:
        pass
    assert len(guard.get_violations()) == 1


def test_summary():
    guard = make_guard()
    guard.enter("task_a", "s1")
    s = guard.summary()
    assert s["total_calls"] == 1
    assert "task_a" in s["call_counts"]