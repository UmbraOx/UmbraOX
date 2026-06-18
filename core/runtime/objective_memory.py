class ObjectiveMemory:

    def __init__(self):

        self.memory = []

    def remember(
        self,
        objective
    ):

        self.memory.append(objective)

    def history(self):

        return self.memory