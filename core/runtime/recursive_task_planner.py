from core.runtime.goal_decomposition_system import (
    GoalDecompositionSystem
)


class RecursiveTaskPlanner:

    def __init__(self):

        self.decomposer = (
            GoalDecompositionSystem()
        )

    def plan(
        self,
        goal
    ):

        return self.decomposer.decompose(goal)