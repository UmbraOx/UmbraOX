class ParallelExecutionEngine:

    def execute(
        self,
        agents,
        tasks
    ):

        results = []

        for agent, task in zip(
            agents,
            tasks
        ):

            results.append(
                agent.execute(task)
            )

        return results