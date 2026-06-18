class GoalDecompositionSystem:

    def decompose(
        self,
        goal
    ):

        return [
            f"{goal} :: phase_1",
            f"{goal} :: phase_2",
            f"{goal} :: phase_3",
            f"{goal} :: phase_4"
        ]