from core.runtime.execution_task import (
    ExecutionTask
)

from core.runtime.recursive_worker_system import (
    RecursiveWorkerSystem
)


class RecursiveExecutionEngine:

    def execute(
        self,
        objectives
    ):

        tasks = []

        for index, objective in enumerate(
            objectives,
            start=1
        ):

            tasks.append(
                ExecutionTask(
                    task_id=f"recursive_{index}",
                    objective=objective
                )
            )

        workers = (
            RecursiveWorkerSystem()
            .spawn_workers(
                len(tasks)
            )
        )

        results = []

        for worker, task in zip(
            workers,
            tasks
        ):

            results.append(
                worker.execute(task)
            )

        return results