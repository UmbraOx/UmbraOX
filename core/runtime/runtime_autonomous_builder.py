from core.runtime.runtime_execution_router import (
    RuntimeExecutionRouter
)

from core.runtime.runtime_generation_pipeline import (
    RuntimeGenerationPipeline
)

from core.runtime.runtime_task_planner import (
    RuntimeTaskPlanner
)

from core.runtime.runtime_wave_executor import (
    RuntimeWaveExecutor
)

from core.runtime.runtime_execution_history import (
    RuntimeExecutionHistory
)

from core.runtime.runtime_recursive_engine import (
    RuntimeRecursiveEngine
)


class RuntimeAutonomousBuilder:

    def __init__(self):

        self.router = RuntimeExecutionRouter()

        self.pipeline = (
            RuntimeGenerationPipeline()
        )

        self.planner = RuntimeTaskPlanner()

        self.executor = RuntimeWaveExecutor()

        self.history = (
            RuntimeExecutionHistory()
        )

        self.recursive = (
            RuntimeRecursiveEngine()
        )

    def build(self, objective):

        domains = self.router.route(
            objective
        )

        generation = self.pipeline.generate(
            domains
        )

        tasks = self.planner.plan(
            objective
        )

        execution = self.executor.execute(
            tasks
        )

        recursive = self.recursive.expand(
            objective
        )

        payload = {
            "objective": objective,
            "domains": domains,
            "generated": generation,
            "execution": execution,
            "recursive": recursive
        }

        self.history.record(payload)

        return payload