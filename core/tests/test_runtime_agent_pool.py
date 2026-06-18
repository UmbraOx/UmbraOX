import pytest
import time
from core.runtime.runtime_agent_pool import RuntimeAgentPool, AgentTask


def test_submit_task():
    pool = RuntimeAgentPool(max_agents=2)
    agent_id, err = pool.submit("t1", "do task 1", lambda obj: "done")
    assert err is None
    assert agent_id is not None


def test_pool_executes_task():
    pool = RuntimeAgentPool(max_agents=2)
    results = []
    def executor(obj):
        results.append(obj)
        return "done"
    pool.submit("t1", "objective_a", executor)
    pool.wait_all(timeout=5)
    assert len(results) == 1
    assert results[0] == "objective_a"


def test_pool_full_returns_error():
    pool = RuntimeAgentPool(max_agents=1)
    import threading
    barrier = threading.Event()
    def slow_executor(obj):
        barrier.wait(timeout=5)
        return "done"
    pool.submit("t1", "task 1", slow_executor)
    time.sleep(0.05)
    _, err = pool.submit("t2", "task 2", lambda o: "done")
    assert err == "pool_full"
    barrier.set()
    pool.wait_all(timeout=5)


def test_completed_tasks_recorded():
    pool = RuntimeAgentPool(max_agents=3)
    pool.submit("t1", "task 1", lambda o: "result1")
    pool.submit("t2", "task 2", lambda o: "result2")
    pool.wait_all(timeout=5)
    completed = pool.get_completed_tasks()
    assert len(completed) == 2


def test_capacity():
    pool = RuntimeAgentPool(max_agents=3)
    assert pool.capacity() == 3


def test_is_not_full():
    pool = RuntimeAgentPool(max_agents=3)
    assert pool.is_full() is False


def test_agent_task_to_dict():
    task = AgentTask("agent_001", "task_1", "do something")
    d = task.to_dict()
    assert d["agent_id"] == "agent_001"
    assert d["task_id"] == "task_1"
    assert d["status"] == "pending"


def test_failed_task_recorded():
    pool = RuntimeAgentPool(max_agents=2)
    def failing_executor(obj):
        raise ValueError("intentional failure")
    pool.submit("t_fail", "fail task", failing_executor)
    pool.wait_all(timeout=5)
    completed = pool.get_completed_tasks()
    assert any(t["status"] == "failed" for t in completed)


def test_wait_all_returns_true():
    pool = RuntimeAgentPool(max_agents=2)
    pool.submit("t1", "quick task", lambda o: "done")
    result = pool.wait_all(timeout=5)
    assert result is True


def test_reset_completed():
    pool = RuntimeAgentPool(max_agents=2)
    pool.submit("t1", "task", lambda o: "done")
    pool.wait_all(timeout=5)
    pool.reset_completed()
    assert len(pool.get_completed_tasks()) == 0