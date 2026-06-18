class ConstructionExecutionRouter:

    def execute(
        self,
        tasks
    ):

        return {
            "executed": len(tasks)
        }