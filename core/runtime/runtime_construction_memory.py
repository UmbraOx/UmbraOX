class RuntimeConstructionMemory:

    def __init__(self):

        self.memory = []

    def remember(self, item):

        self.memory.append(item)

    def all(self):

        return self.memory