class RecursiveConstructionEngine:

    def construct(
        self,
        tasks
    ):

        results = []

        for task in tasks:

            results.append({
                "constructed": task["objective"]
            })

        return results