class RecursiveConstructionPlanner:

    def build(self, objective):

        return {
            "objective": objective,
            "stages": [
                "architecture",
                "runtime",
                "validation",
                "deployment"
            ]
        }