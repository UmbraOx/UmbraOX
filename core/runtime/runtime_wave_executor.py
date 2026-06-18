from core.runtime.runtime_worker_pool import (
    RuntimeWorkerPool
)

from core.runtime.runtime_task_executor import (
    RuntimeTaskExecutor
)


class RuntimeWaveExecutor:

    def __init__(self):

        self.pool = RuntimeWorkerPool()

        self.executor = RuntimeTaskExecutor()

    def execute(self, tasks):

        workers = self.pool.spawn(len(tasks))

        results = []

        for worker, task in zip(workers, tasks):

            results.append(
                self.executor.execute(
                    worker,
                    task["objective"]
                )
            )

        return results