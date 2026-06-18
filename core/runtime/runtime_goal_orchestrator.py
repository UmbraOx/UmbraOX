class RuntimeGoalOrchestrator:
    def __init__(self):
        self.active_goals = []

    def register_goal(self, goal: str):
        self.active_goals.append(goal)

        return {
            "goal": goal,
            "status": "registered"
        }

    def get_goals(self):
        return self.active_goals