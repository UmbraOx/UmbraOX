from collections import deque
from core.runtime.umbra_task_schema import UmbraTask


class UmbraTaskQueueManager:
    """
    Central queue used by:
    - BossAgent
    - Spine
    - GUI
    - Generation engine
    """

    def __init__(self):
        self.queue = deque()

    def add_task(self, task: UmbraTask):
        self.queue.append(task)

    def pop_task(self):
        if not self.queue:
            return None
        return self.queue.popleft()

    def reprioritize(self, index: int, direction: str):
        """
        Move tasks up/down in queue.
        """
        q = list(self.queue)

        if index < 0 or index >= len(q):
            return

        if direction == "up" and index > 0:
            q[index], q[index - 1] = q[index - 1], q[index]

        if direction == "down" and index < len(q) - 1:
            q[index], q[index + 1] = q[index + 1], q[index]

        self.queue = deque(q)

    def list_tasks(self):
        return list(self.queue)