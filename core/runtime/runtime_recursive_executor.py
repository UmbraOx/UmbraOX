class RuntimeRecursiveExecutor:
    def __init__(self):
        self.completed = []

    def execute_recursive(self, tasks):
        results = []

        for task in tasks:
            outcome = {
                "task": task,
                "status": "completed"
            }

            results.append(outcome)
            self.completed.append(outcome)

        return results