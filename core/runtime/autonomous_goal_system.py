class AutonomousGoalSystem:

    def __init__(self):

        self.goals = []

    def register_goal(
        self,
        goal
    ):

        self.goals.append(goal)

    def list_goals(self):

        return self.goals