class RuntimeRecursiveMutator:

    def mutate(
        self,
        modules
    ):
        mutated = []

        for module in modules:
            mutated.append({
                "module": module,
                "mutated": True
            })

        return mutated