class DynamicObjectiveExpander:

    def expand(
        self,
        objective
    ):

        return [
            objective,
            f"{objective} :: expansion_1",
            f"{objective} :: expansion_2"
        ]