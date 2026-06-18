class SystemConstructionGraph:

    def build(
        self,
        objectives
    ):

        graph = {}

        previous = None

        for objective in objectives:

            graph[objective] = []

            if previous:

                graph[previous].append(
                    objective
                )

            previous = objective

        return graph