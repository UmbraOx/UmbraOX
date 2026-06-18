# core/runtime/resource_guardian.py

class ResourceGuardian:
    """
    Prevents runaway execution loops and limits system load.
    """

    def __init__(self, max_tasks=50):
        self.max_tasks = max_tasks
        self.task_count = 0

    def allow(self):
        return self.task_count < self.max_tasks

    def register_task(self):
        self.task_count += 1

    def reset(self):
        self.task_count = 0


guardian = ResourceGuardian()