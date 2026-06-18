class RuntimeContinuousLoop:

    def __init__(self):

        self.iterations = 0

    def cycle(self):

        self.iterations += 1

        return {
            "status": "running",
            "iterations": self.iterations
        }