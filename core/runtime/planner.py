# core/runtime/planner.py


class Planner:
    def make_plan(self, user_input):
        # normalize everything into a single step plan
        return [
            {
                "tool": "router",
                "input": user_input
            }
        ]