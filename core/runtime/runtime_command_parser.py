class RuntimeCommandParser:

    def parse(self, objective):

        return {
            "objective": objective,
            "commands": [
                "analyze",
                "plan",
                "generate",
                "validate",
                "execute"
            ]
        }