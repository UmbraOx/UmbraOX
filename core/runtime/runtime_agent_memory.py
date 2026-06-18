class RuntimeAgentMemory:
    def __init__(self):
        self.memory = {}

    def remember(self, agent, item):
        self.memory.setdefault(agent, [])
        self.memory[agent].append(item)

    def recall(self, agent):
        return self.memory.get(agent, [])