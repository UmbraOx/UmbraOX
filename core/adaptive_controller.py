from core.feedback_memory import FeedbackMemory
from core.planner import Planner
from core.validator import PlanValidator


class AdaptiveController:

    def __init__(self):
        self.feedback = FeedbackMemory()
        self.planner = Planner()
        self.validator = PlanValidator()

    def evaluate(self, task, results):

        """
        Decides whether we need to replan
        """

        if not results:
            return True

        for r in results:
            if isinstance(r, dict) and "error" in r:
                return True

        return False

    def replan_if_needed(self, task, results):

        if self.evaluate(task, results):

            print("[ADAPTIVE] Replanning task...")

            plan = self.planner.create_plan(task)
            plan = self.validator.validate(plan)

            return plan

        return None