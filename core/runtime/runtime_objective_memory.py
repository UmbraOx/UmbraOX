class RuntimeObjectiveMemory:

    def __init__(self):

        self.objectives = []

    def remember(self, objective):

        self.objectives.append(
            objective
        )

    def all(self):

        return self.objectives