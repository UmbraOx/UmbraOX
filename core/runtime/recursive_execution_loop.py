class RecursiveExecutionLoop:

    def execute(
        self,
        chain
    ):

        completed = []

        for task in chain["chain"]:

            completed.append({
                "task": task,
                "status": "completed"
            })

        return completed