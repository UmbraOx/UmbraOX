class ProjectObjectiveEngine:

    def build_objective(
        self,
        prompt
    ):

        return {
            "objective": prompt,
            "priority": "high"
        }