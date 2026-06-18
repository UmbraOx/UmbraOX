class ExecutionGraphEngine:

    def build(self, tasks):

        graph = {}

        previous = None

        for task in tasks:

            graph[task.task_id] = []

            if previous:

                graph[previous].append(
                    task.task_id
                )

            previous = task.task_id

        return graph