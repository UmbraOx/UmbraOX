# C:\Umbra\core\runtime\task_queue.py

from collections import deque
from datetime import datetime


class TaskQueue:
    """
    Minimal stable task queue used across runtime imports.
    This replaces all missing/fragmented queue implementations.
    """

    def __init__(self):
        self.queue = deque()
        self.history = []

    def add(self, task):
        entry = {
            "task": task,
            "created_at": datetime.now().isoformat(),
            "status": "queued",
        }
        self.queue.append(entry)
        return entry

    def pop(self):
        if not self.queue:
            return None

        task = self.queue.popleft()
        task["status"] = "completed"
        self.history.append(task)
        return task

    def size(self):
        return len(self.queue)

    def to_list(self):
        return list(self.queue)