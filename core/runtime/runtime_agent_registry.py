class RuntimeAgentRegistry:
    """
    Central registry for runtime agents.
    Fixed to support both object-based and dict-based agents.
    """

    def __init__(self):
        self.agents = {}

    def register(self, name_or_agent, role=None):
        """
        Supports:
        - register(agent_object)
        - register(name, role)
        """
        if role is None:
            agent = name_or_agent
            self.agents[getattr(agent, "name", str(agent))] = agent
        else:
            self.agents[name_or_agent] = {
                "name": name_or_agent,
                "role": role,
                "active": True,
            }

    def get_agent(self, name):
        return self.agents.get(name)

    def list_agents(self):
        return list(self.agents.keys())

    def all(self):
        return self.agents