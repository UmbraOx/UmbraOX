from __future__ import annotations


class RuntimeGoalDecomposer:
    def decompose_goal(self, goal: str) -> list[str]:
        return [
            f"Analyze goal: {goal}",
            f"Plan implementation: {goal}",
            f"Execute implementation: {goal}",
            f"Validate implementation: {goal}",
        ]

    def prioritize_tasks(self, tasks: list[str]) -> list[str]:
        return sorted(tasks)