from __future__ import annotations

from core.runtime.runtime_autonomous_planner import RuntimeAutonomousPlanner
from core.runtime.runtime_autonomous_executor import RuntimeAutonomousExecutor


class RuntimeOrchestrator:
    def __init__(self):
        self.planner = RuntimeAutonomousPlanner()
        self.executor = RuntimeAutonomousExecutor()

    def execute_goal(self, goal: str) -> dict:
        plan = self.planner.generate_plan(goal)
        return self.executor.execute_plan(plan)