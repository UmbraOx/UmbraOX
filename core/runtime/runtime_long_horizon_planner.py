class RuntimeLongHorizonPlanner:

    def expand(self, objective):

        return [
            f"{objective} :: milestone_1",
            f"{objective} :: milestone_2",
            f"{objective} :: milestone_3",
            f"{objective} :: milestone_4",
            f"{objective} :: milestone_5"
        ]