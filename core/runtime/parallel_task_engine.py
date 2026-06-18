class ParallelTaskEngine:

    def execute(
        self,
        workers,
        tasks
    ):

        results = []

        for worker, task in zip(
            workers,
            tasks
        ):

            results.append(
                worker.execute(task)
            )

        return results