class AgentRegistry:

    def __init__(self):

        self.agents = {}

    def register(self, name, role):

        self.agents[name] = {
            "role": role,
            "status": "active"
        }

    def list_agents(self):

        return self.agents