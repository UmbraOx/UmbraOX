class RuntimeAutonomousController:

    def __init__(self):

        self.state = "idle"

    def control(
        self,
        objective
    ):

        self.state = "active"

        return {
            "status": "controlled",
            "objective": objective
        }