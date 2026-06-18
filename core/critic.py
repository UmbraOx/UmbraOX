class Critic:

    def review(self, plan):

        if not isinstance(plan, dict):
            return False

        steps = plan.get("steps")

        if not isinstance(steps, list):
            return False

        for step in steps:

            if "action" not in step:
                return False

            if "path" not in step:
                return False

        return True