class ExecutionRecoveryEngine:

    def recover(
        self,
        failed_task
    ):

        return {
            "task": failed_task,
            "recovered": True
        }