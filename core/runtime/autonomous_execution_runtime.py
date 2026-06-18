from core.runtime.execution_task import (
    ExecutionTask
)

from core.runtime.task_worker import (
    TaskWorker
)

from core.runtime.parallel_task_engine import (
    ParallelTaskEngine
)


class AutonomousExecutionRuntime:

    def execute_objectives(
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
                    task_id=f"task_{index}",
                    objective=objective
                )
            )

        workers = [

            TaskWorker(
                f"worker_{i}"
            )

            for i in range(
                1,
                len(tasks) + 1
            )
        ]

        engine = (
            ParallelTaskEngine()
        )

        return engine.execute(
            workers,
            tasks
        )