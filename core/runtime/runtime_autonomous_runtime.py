from .runtime_task_store import RuntimeTaskStore
from .runtime_task_scheduler import RuntimeTaskScheduler
from .runtime_task_worker import RuntimeTaskWorker
from .runtime_task_engine import RuntimeTaskEngine


class RuntimeAutonomousRuntime:
    """
    Full persistent autonomous execution system.
    """

    def __init__(self, orchestrator):
        self.store = RuntimeTaskStore()
        self.scheduler = RuntimeTaskScheduler(self.store)
        self.worker = RuntimeTaskWorker(orchestrator)
        self.engine = RuntimeTaskEngine(self.store, self.scheduler, self.worker)

    def start(self):
        return self.engine.run_forever()

    def tick(self):
        return self.engine.tick()

    def stop(self):
        self.engine.stop()

    def status(self):
        return {
            "queued": len(self.store.list("queued")),
            "running": len(self.store.list("running")),
            "completed": len(self.store.list("completed")),
            "failed": len(self.store.list("failed")),
        }