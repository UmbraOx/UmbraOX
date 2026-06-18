class RuntimePriorityScheduler:

    def __init__(self):

        self.queue = []

    def schedule(
        self,
        priority,
        task
    ):

        self.queue.append(
            (priority, task)
        )

        self.queue.sort(
            key=lambda x: x[0]
        )

    def next_task(self):

        if not self.queue:
            return None

        return self.queue.pop(0)