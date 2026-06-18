class RuntimeGoalMemory:

    def __init__(self):
        self.goals = []

    def store(
        self,
        goal
    ):
        self.goals.append(goal)

    def all(self):
        return self.goals