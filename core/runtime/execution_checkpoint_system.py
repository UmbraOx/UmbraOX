class ExecutionCheckpointSystem:

    def checkpoint(
        self,
        state
    ):

        return {
            "checkpoint": True,
            "state": state
        }