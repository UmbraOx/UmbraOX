class AgentSupervisor:

    def __init__(self):

        self.agents = []

    def register(
        self,
        agent
    ):

        self.agents.append(agent)

    def list_agents(self):

        return [
            agent.name
            for agent in self.agents
        ]