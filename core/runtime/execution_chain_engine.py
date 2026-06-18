class ExecutionChainEngine:

    def build_chain(
        self,
        tasks
    ):

        return {
            "chain": tasks,
            "length": len(tasks)
        }