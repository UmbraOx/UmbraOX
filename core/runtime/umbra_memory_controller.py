from core.runtime.runtime_persistent_brain import (
    RuntimePersistentBrain
)

from core.runtime.runtime_goal_memory import (
    RuntimeGoalMemory
)


class UmbraMemoryController:

    def __init__(self):
        self.brain = (
            RuntimePersistentBrain()
        )

        self.goals = (
            RuntimeGoalMemory()
        )

    def remember_objective(
        self,
        objective
    ):
        self.brain.remember({
            "objective": objective
        })

        self.goals.store(
            objective
        )

    def snapshot(self):
        return {
            "brain": self.brain.load(),
            "goals": self.goals.all()
        }