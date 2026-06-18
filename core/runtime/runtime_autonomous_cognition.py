from core.runtime.runtime_cognition_memory import (
    RuntimeCognitionMemory
)

from core.runtime.runtime_long_horizon_planner import (
    RuntimeLongHorizonPlanner
)


class RuntimeAutonomousCognition:

    def __init__(self):

        self.memory = (
            RuntimeCognitionMemory()
        )

        self.planner = (
            RuntimeLongHorizonPlanner()
        )

    def process(self, objective):

        milestones = (
            self.planner.expand(
                objective
            )
        )

        self.memory.think(
            objective
        )

        return {
            "objective": objective,
            "milestones": milestones,
            "cognition":
            self.memory.history()
        }