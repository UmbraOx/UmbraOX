class ExecutionTask:

    def __init__(
        self,
        task_id,
        objective,
        domain="runtime",
        priority=1
    ):

        self.task_id = task_id
        self.objective = objective
        self.domain = domain
        self.priority = priority

        self.status = "pending"

    def start(self):

        self.status = "running"

    def complete(self):

        self.status = "completed"

    def fail(self):

        self.status = "failed"