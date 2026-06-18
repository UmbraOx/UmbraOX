class ConstructionDependencyResolver:

    def resolve(
        self,
        graph
    ):

        return {
            "resolved": True,
            "nodes": len(graph)
        }