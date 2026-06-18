class RuntimeRecursiveScheduler:

    def schedule(
        self,
        tasks
    ):
        scheduled = []

        for index, task in enumerate(tasks):
            scheduled.append({
                "wave": index + 1,
                "task": task
            })

        return scheduled