class RecursivePlanningEngine:

    def expand(
        self,
        objective
    ):

        text = objective["objective"]

        return [
            f"{text} :: architecture",
            f"{text} :: runtime",
            f"{text} :: agents",
            f"{text} :: validation",
            f"{text} :: deployment"
        ]