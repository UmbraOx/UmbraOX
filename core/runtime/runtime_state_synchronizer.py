class RuntimeStateSynchronizer:

    def synchronize(
        self,
        state
    ):

        return {
            "synchronized": True,
            "state": state
        }