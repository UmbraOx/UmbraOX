from core.runtime.task_worker import (
    TaskWorker
)


class RecursiveWorkerSystem:

    def spawn_workers(
        self,
        count
    ):

        workers = []

        for index in range(
            1,
            count + 1
        ):

            workers.append(
                TaskWorker(
                    f"recursive_worker_{index}"
                )
            )

        return workers