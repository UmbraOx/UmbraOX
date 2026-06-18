class ConstructionTaskGraph:

    def build(
        self,
        tasks
    ):

        return {
            "nodes": tasks,
            "edges": len(tasks) - 1
        }