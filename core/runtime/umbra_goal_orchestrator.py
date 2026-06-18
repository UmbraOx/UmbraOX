from core.runtime.runtime_goal_engine import (
    RuntimeGoalEngine
)

from core.runtime.runtime_recursive_scheduler import (
    RuntimeRecursiveScheduler
)


class UmbraGoalOrchestrator:

    def __init__(self):
        self.goals = (
            RuntimeGoalEngine()
        )

        self.scheduler = (
            RuntimeRecursiveScheduler()
        )

    def orchestrate(
        self,
        objective
    ):
        expanded = (
            self.goals.expand(
                objective
            )
        )

        return self.scheduler.schedule(
            expanded
        )