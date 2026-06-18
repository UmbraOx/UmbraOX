from concurrent.futures import ThreadPoolExecutor


class RuntimeWorkerPool:

    def __init__(
        self,
        workers=4
    ):

        self.workers = workers

        self.executor = (
            ThreadPoolExecutor(
                max_workers=workers
            )
        )

    def execute(
        self,
        function,
        tasks
    ):

        futures = []

        for task in tasks:

            future = (
                self.executor.submit(
                    function,
                    task
                )
            )

            futures.append(future)

        results = []

        for future in futures:

            try:

                results.append(
                    future.result()
                )

            except Exception as e:

                results.append(
                    {
                        "success": False,
                        "error": str(e)
                    }
                )

        return results