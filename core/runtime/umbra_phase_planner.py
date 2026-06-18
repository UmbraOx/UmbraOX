class UmbraPhasePlanner:

    def build(
        self,
        goals
    ):

        phases = []

        for index, goal in enumerate(goals):

            phases.append({
                "phase": index + 1,
                "objective": goal
            })

        return phases