import pytest


def test_queue():
    # This test covers the legacy RuntimeQueue stub.
    # The full priority queue is tested in test_runtime_task_queue.py
    from core.runtime.runtime_task_queue import RuntimeTaskQueue
    queue = RuntimeTaskQueue()
    queue.enqueue("task_1", "do something", priority=5)
    assert queue.size() == 1
    task = queue.dequeue()
    assert task.task_id == "task_1"
    assert queue.size() == 0