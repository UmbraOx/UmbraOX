# core/runtime/autonomous_planning_loop.py

from core.runtime.autonomous_architect import (
    AutonomousArchitect
)

from core.runtime.improvement_planner import (
    ImprovementPlanner
)

from core.runtime.task_generator import (
    TaskGenerator
)


class AutonomousPlanningLoop:

    def __init__(self):

        self.architect = AutonomousArchitect()

        self.planner = ImprovementPlanner()

        self.generator = TaskGenerator()

    # -------------------------------------------------
    # RUN
    # -------------------------------------------------

    def run(self):

        review = self.architect.review_project()

        plans = self.planner.generate_plan(
            review
        )

        tasks = self.generator.generate_tasks(
            plans
        )

        result = {
            "review": review,
            "plans": plans,
            "tasks": tasks
        }

        print(
            "[AUTONOMOUS_PLANNING] complete"
        )

        return result