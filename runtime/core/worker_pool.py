# core/runtime/worker_pool.py

import threading
import time

class WorkerPool:
    def __init__(self, max_workers=4):
        self.max_workers = max_workers
        self.active = True

    def execute(self, task, executor_fn):
        if not self.active:
            return

        def run():
            try:
                executor_fn(task)
            except Exception as e:
                print(f"[Worker Error] {task.task_id}: {e}")

        threading.Thread(target=run, daemon=True).start()

    def pause(self):
        self.active = False

    def resume(self):
        self.active = True