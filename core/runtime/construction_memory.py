class ConstructionMemory:

    def __init__(self):

        self.history = []

    def record(
        self,
        event
    ):

        self.history.append(event)

    def all(self):

        return self.history