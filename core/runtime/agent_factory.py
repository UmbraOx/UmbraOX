class AgentFactory:

    def generate(self, proposal):

        title = proposal.get(
            "title",
            "agent"
        )

        return [{
            "name": f"{title} Agent",
            "role": "specialist",
            "status": "planned"
        }]