class DynamicToolchainBuilder:

    def build(
        self,
        objective
    ):

        return {
            "objective": objective,
            "toolchain": [
                "generator",
                "validator",
                "deployer"
            ]
        }