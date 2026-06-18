from core.runtime.runtime_task_state import (
    RuntimeTaskState
)


class RuntimeExecutionDispatcher:

    def __init__(self):

        self.state = RuntimeTaskState()

    def dispatch(
        self,
        objectives,
        workers
    ):

        results = []

        for index, objective in enumerate(objectives):

            worker = (
                workers[
                    index % len(workers)
                ]
            )

            task = self.state.create(
                objective,
                worker
            )

            results.append(
                self.state.complete(task)
            )

        return results