class RecursivePhaseGenerator:

    def generate(
        self,
        objective
    ):

        return [
            f"{objective} :: initialize",
            f"{objective} :: construct",
            f"{objective} :: validate",
            f"{objective} :: deploy"
        ]