import pytest
from core.runtime.runtime_task_queue import RuntimeTaskQueue, QueuedTask


@pytest.fixture
def queue():
    return RuntimeTaskQueue()


def test_enqueue_returns_task(queue):
    task = queue.enqueue("t1", "do something")
    assert isinstance(task, QueuedTask)
    assert task.task_id == "t1"


def test_dequeue_returns_highest_priority(queue):
    queue.enqueue("low", "low priority task", priority=8)
    queue.enqueue("high", "high priority task", priority=1)
    queue.enqueue("mid", "medium priority task", priority=5)
    task = queue.dequeue()
    assert task.task_id == "high"


def test_dequeue_empty_returns_none(queue):
    assert queue.dequeue() is None


def test_size_after_enqueue(queue):
    queue.enqueue("a", "task a")
    queue.enqueue("b", "task b")
    assert queue.size() == 2


def test_size_after_dequeue(queue):
    queue.enqueue("a", "task a")
    queue.dequeue()
    assert queue.size() == 0


def test_is_empty_true(queue):
    assert queue.is_empty() is True


def test_is_empty_false(queue):
    queue.enqueue("t", "task")
    assert queue.is_empty() is False


def test_complete_marks_done(queue):
    queue.enqueue("t1", "task")
    queue.dequeue()
    result = queue.complete("t1")
    assert result is True
    assert queue._tasks["t1"].status == "completed"


def test_fail_marks_failed(queue):
    queue.enqueue("t1", "task")
    queue.dequeue()
    result = queue.fail("t1", error="something broke")
    assert result is True
    assert queue._tasks["t1"].status == "failed"


def test_processed_recorded_on_complete(queue):
    queue.enqueue("t1", "task")
    queue.dequeue()
    queue.complete("t1")
    assert len(queue.processed) == 1


def test_list_queued(queue):
    queue.enqueue("a", "task a")
    queue.enqueue("b", "task b")
    queued = queue.list_queued()
    assert len(queued) == 2


def test_peek_returns_highest_priority(queue):
    queue.enqueue("low", "low", priority=9)
    queue.enqueue("high", "high", priority=1)
    task = queue.peek()
    assert task.task_id == "high"


def test_clear_empties_queue(queue):
    queue.enqueue("a", "task")
    queue.enqueue("b", "task")
    queue.clear()
    assert queue.is_empty() is True


def test_get_task_by_id(queue):
    queue.enqueue("t99", "special task", priority=3)
    task = queue.get_task("t99")
    assert task is not None
    assert task.objective == "special task"


def test_task_to_dict():
    task = QueuedTask("t1", "test", 2, {"key": "val"})
    d = task.to_dict()
    assert d["task_id"] == "t1"
    assert d["priority"] == 2
    assert d["metadata"]["key"] == "val"