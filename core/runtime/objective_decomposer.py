class ObjectiveDecomposer:

    def decompose(
        self,
        objective
    ):

        text = objective["objective"]

        return {
            "planning": f"{text} planning",
            "implementation": f"{text} implementation",
            "validation": f"{text} validation"
        }