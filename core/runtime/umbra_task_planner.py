import json


class UmbraTaskPlanner:
    """
    Converts high-level goals into executable steps.
    """

    def __init__(self, llm_engine=None):
        self.llm = llm_engine

    def decompose(self, goal: str):
        """
        Produces structured steps from goal.
        """

        # fallback deterministic planning if no LLM
        if not self.llm:
            return [f"Analyze goal: {goal}", "Execute implementation", "Verify result"]

        prompt = f"""
Break this goal into structured executable steps:

GOAL:
{goal}

Return JSON list only:
["step1", "step2", "step3"]
"""

        raw = self.llm(prompt)

        try:
            return json.loads(raw)
        except:
            return [goal, "execute", "verify"]