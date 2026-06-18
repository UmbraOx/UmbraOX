class AgentContextMemory:

    def __init__(self):

        self.memory = {}

    def store(
        self,
        agent,
        key,
        value
    ):

        if agent not in self.memory:
            self.memory[agent] = {}

        self.memory[agent][key] = value

    def recall(
        self,
        agent,
        key,
        default=None
    ):

        if agent not in self.memory:
            return default

        return self.memory[agent].get(
            key,
            default
        )