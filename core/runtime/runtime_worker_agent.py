class RuntimeWorkerAgent:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.active = True
        self.last_result = None

    def execute(self, objective):
        result = {
            "worker": self.name,
            "role": self.role,
            "objective": objective,
            "status": "completed"
        }
        self.last_result = result
        return result