class LiveConstructionOrchestrator:

    def orchestrate(
        self,
        objective
    ):

        return {
            "objective": objective,
            "status": "constructing"
        }