from core.runtime.umbra_goal_orchestrator import (
    UmbraGoalOrchestrator
)

from core.runtime.umbra_execution_pipeline import (
    UmbraExecutionPipeline
)

from core.runtime.umbra_validation_pipeline import (
    UmbraValidationPipeline
)

from core.runtime.umbra_recursive_core import (
    UmbraRecursiveCore
)


class UmbraAutonomousController:

    def __init__(self):
        self.goals = (
            UmbraGoalOrchestrator()
        )

        self.execution = (
            UmbraExecutionPipeline()
        )

        self.validation = (
            UmbraValidationPipeline()
        )

        self.recursive = (
            UmbraRecursiveCore()
        )

    def execute(
        self,
        objective
    ):
        tasks = (
            self.goals.orchestrate(
                objective
            )
        )

        generated = (
            self.execution.execute(
                objective
            )
        )

        recursive = (
            self.recursive.evolve(
                objective
            )
        )

        valid = (
            self.validation.validate(
                [generated]
            )
        )

        return {
            "objective": objective,
            "tasks": tasks,
            "generated": generated,
            "recursive": recursive,
            "validated": valid
        }