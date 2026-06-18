# core/runtime/worker_pool.py

import threading
from queue import Queue
from core.runtime.kill_switch import kill_switch


class WorkerPool:
    """
    Minimal async worker pool for executing routed tasks.
    """

    def __init__(self, executor, num_workers=2):
        self.executor = executor
        self.queue = Queue()
        self.workers = []
        self.num_workers = num_workers
        self.running = False

    def start(self):
        self.running = True

        for _ in range(self.num_workers):
            t = threading.Thread(target=self.worker_loop, daemon=True)
            t.start()
            self.workers.append(t)

    def stop(self):
        self.running = False

    def submit(self, task_id, routed_steps):
        self.queue.put((task_id, routed_steps))

    def worker_loop(self):
        while self.running:

            if kill_switch.active:
                continue

            try:
                task_id, steps = self.queue.get(timeout=0.5)
            except:
                continue

            self.executor.execute(steps, task_id=task_id)
            self.queue.task_done()


worker_pool = WorkerPool