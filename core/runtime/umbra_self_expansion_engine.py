class UmbraSelfExpansionEngine:

    def expand(
        self,
        runtime
    ):
        runtime["expanded"] = True

        return runtime