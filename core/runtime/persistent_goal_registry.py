class PersistentGoalRegistry:

    def __init__(self):

        self.registry = []

    def add(
        self,
        goal
    ):

        self.registry.append(goal)

    def all(self):

        return self.registry