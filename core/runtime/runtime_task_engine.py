import time


class RuntimeTaskEngine:
    """
    Main autonomous loop engine.
    """

    def __init__(self, store, scheduler, worker):
        self.store = store
        self.scheduler = scheduler
        self.worker = worker
        self.running = False
        self.history = []

    def tick(self):
        tasks = self.scheduler.get_next_tasks()

        results = []

        for task in tasks:
            self.scheduler.mark_running(task.id)

            result = self.worker.execute(task)

            if result["status"] == "completed":
                self.scheduler.mark_done(task.id, result["result"])
            else:
                self.scheduler.mark_failed(task.id, result.get("error"))

            results.append(result)

        return results

    def run_forever(self, delay=2):
        self.running = True

        while self.running:
            self.tick()
            time.sleep(delay)

    def stop(self):
        self.running = False