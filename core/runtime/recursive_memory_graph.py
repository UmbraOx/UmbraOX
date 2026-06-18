class RecursiveMemoryGraph:

    def build(
        self,
        goals
    ):

        graph = {}

        previous = None

        for goal in goals:

            graph[goal] = []

            if previous:

                graph[previous].append(goal)

            previous = goal

        return graph