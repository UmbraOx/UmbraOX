class RuntimeExecutionGuard:

    def check(self, objective):

        return {
            "safe": True,
            "objective": objective
        }