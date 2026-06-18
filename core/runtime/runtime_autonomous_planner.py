from __future__ import annotations

from core.runtime.runtime_goal_decomposer import RuntimeGoalDecomposer


class RuntimeAutonomousPlanner:
    def __init__(self):
        self.decomposer = RuntimeGoalDecomposer()

    def generate_plan(self, goal: str) -> dict:
        tasks = self.decomposer.decompose_goal(goal)

        return {
            "goal": goal,
            "tasks": tasks,
            "status": "planned",
        }