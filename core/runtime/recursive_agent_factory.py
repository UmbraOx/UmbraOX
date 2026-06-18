class RecursiveAgentFactory:

    def create_agents(
        self,
        objective
    ):

        return [
            {
                "name": "architect_agent"
            },
            {
                "name": "builder_agent"
            },
            {
                "name": "validator_agent"
            }
        ]