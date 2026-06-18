class UmbraMultiAgentDirector:

    def direct(
        self,
        objective
    ):
        return [
            {
                "agent": "architect",
                "objective": objective
            },
            {
                "agent": "coder",
                "objective": objective
            },
            {
                "agent": "reviewer",
                "objective": objective
            }
        ]