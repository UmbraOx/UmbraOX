class RuntimeStrategyEngine:

    def __init__(self):

        self.strategies = []

    def build_strategy(
        self,
        goal
    ):

        strategy = {
            "goal": goal,
            "steps": [
                "analyze",
                "plan",
                "execute"
            ]
        }

        self.strategies.append(strategy)

        return {
            "status": "strategy_created",
            "strategy": strategy
        }