class RuntimeRecursiveExpansion:

    def expand(
        self,
        objectives
    ):

        expanded = []

        for item in objectives:

            expanded.append(
                f"{item} :: recursive_expansion"
            )

        return expanded