from core.runtime.recursive_task_planner import (
    RecursiveTaskPlanner
)

from core.runtime.execution_wave_engine import (
    ExecutionWaveEngine
)


class AutonomousConstructionRuntime:

    def __init__(self):

        self.planner = (
            RecursiveTaskPlanner()
        )

        self.wave_engine = (
            ExecutionWaveEngine()
        )

    def build(
        self,
        objective
    ):

        phases = (
            self.planner.plan(
                objective
            )
        )

        waves = (
            self.wave_engine.generate(
                phases
            )
        )

        return {
            "objective": objective,
            "phases": phases,
            "waves": waves
        }