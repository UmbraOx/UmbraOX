class HierarchicalTaskEngine:

    def hierarchy(
        self,
        tasks
    ):

        return {
            "levels": len(tasks),
            "tasks": tasks
        }