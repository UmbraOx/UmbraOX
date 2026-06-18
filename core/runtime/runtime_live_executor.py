class RuntimeLiveExecutor:

    def __init__(self):

        self.executions = []

    def execute(
        self,
        task
    ):

        result = {
            "task": task,
            "status": "executed"
        }

        self.executions.append(result)

        return result