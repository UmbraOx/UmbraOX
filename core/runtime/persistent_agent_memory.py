class PersistentAgentMemory:

    def __init__(self):

        self.memory = {}

    def remember(
        self,
        agent,
        data
    ):

        self.memory[agent] = data

    def recall(
        self,
        agent
    ):

        return self.memory.get(agent)