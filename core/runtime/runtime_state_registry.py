class RuntimeAgentRegistry:

    def __init__(self):
        self.agents = {}

    def register(self, name, role):
        self.agents[name] = role

    def all(self):
        return self.agents