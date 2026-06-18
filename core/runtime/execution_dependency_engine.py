class ExecutionDependencyEngine:

    def build_dependencies(self, tasks):
        graph = {}

        previous = None

        for task in tasks:
            name = task["domain"]

            if previous:
                graph[name] = [previous]
            else:
                graph[name] = []

            previous = name

        return graph