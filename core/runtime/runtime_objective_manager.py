class RuntimeObjectiveManager:

    def __init__(self):

        self.objectives = []

    def create_objective(
        self,
        objective
    ):

        self.objectives.append(objective)

        return {
            "status": "objective_created",
            "objective": objective
        }

    def get_objectives(self):

        return self.objectives