from core.runtime.umbra_task_schema import UmbraTask


class UmbraGenerationDispatchBridge:
    """
    Converts generation requests into queue tasks.
    """

    def __init__(self, task_queue, generation_engine, logger=None):

        self.queue = task_queue
        self.engine = generation_engine
        self.logger = logger

    def submit(self, task_type: str, prompt: str, priority: int = 5):

        task = UmbraTask(
            task_type=task_type,
            prompt=prompt,
            priority=priority
        )

        self.queue.add_task(task)

        if self.logger:
            self.logger.log_event({
                "event": "task_submitted",
                "type": task_type,
                "priority": priority
            })

        return task