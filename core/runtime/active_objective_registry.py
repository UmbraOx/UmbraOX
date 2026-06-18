class ActiveObjectiveRegistry:

    def __init__(self):

        self.objectives = []

    def add(
        self,
        objective
    ):

        self.objectives.append(objective)

    def all(self):

        return self.objectives