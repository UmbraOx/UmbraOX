class RuntimeRecursiveReasoner:

    def __init__(self):

        self.depth = 0

    def recursive_reason(
        self,
        objective
    ):

        self.depth += 1

        return {
            "status": "recursive_complete",
            "objective": objective,
            "depth": self.depth
        }