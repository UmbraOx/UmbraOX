from core.runtime.autonomous_goal_engine import AutonomousGoalEngine
from core.runtime.goal_decomposition_engine import GoalDecompositionEngine


class AutonomousUpgradeOrchestrator:

    def __init__(self):

        self.goals = AutonomousGoalEngine()
        self.decomposer = GoalDecompositionEngine()

    def process(self, prompt):

        goal = self.goals.create_goal(prompt)

        tasks = self.decomposer.decompose(goal)

        return {
            "goal": goal,
            "tasks": tasks
        }