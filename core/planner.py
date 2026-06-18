# core/planner.py

class Planner:
    """
    Minimal stable planner layer.
    Converts raw input into a normalized plan format.
    """

    def make_plan(self, user_input: str):
        """
        Always returns a dict with 'steps'
        so router + boss_agent never break.
        """

        return {
            "steps": [
                {
                    "tool": "execute",
                    "args": {
                        "task": user_input
                    }
                }
            ]
        }