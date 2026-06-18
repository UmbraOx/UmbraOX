# core/runtime/task_scheduler.py

import heapq
import time

class Task:
    def __init__(self, task_id, priority, payload):
        self.task_id = task_id
        self.priority = priority
        self.payload = payload
        self.timestamp = time.time()

    def __lt__(self, other):
        return (self.priority, self.timestamp) < (other.priority, other.timestamp)


class TaskScheduler:
    def __init__(self):
        self.queue = []

    def add_task(self, task):
        heapq.heappush(self.queue, task)

    def reprioritize(self, task_id, new_priority):
        for task in self.queue:
            if task.task_id == task_id:
                task.priority = new_priority
                break
        heapq.heapify(self.queue)

    def get_next_task(self):
        if not self.queue:
            return None
        return heapq.heappop(self.queue)