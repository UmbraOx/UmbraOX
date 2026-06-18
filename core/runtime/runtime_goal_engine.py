class RuntimeGoalEngine:
    def generate_goals(self, objective):
        return [
            f"{objective} :: planning",
            f"{objective} :: execution",
            f"{objective} :: validation",
        ]

    def expand(self, objective):
        return self.generate_goals(objective)