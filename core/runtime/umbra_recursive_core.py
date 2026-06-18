from core.runtime.runtime_recursive_reasoner import (
    RuntimeRecursiveReasoner
)

from core.runtime.runtime_recursive_mutator import (
    RuntimeRecursiveMutator
)


class UmbraRecursiveCore:

    def __init__(self):
        self.reasoner = (
            RuntimeRecursiveReasoner()
        )

        self.mutator = (
            RuntimeRecursiveMutator()
        )

    def evolve(
        self,
        objective
    ):
        reasoning = (
            self.reasoner.reason(
                objective
            )
        )

        mutation = (
            self.mutator.mutate(
                reasoning
            )
        )

        return {
            "reasoning": reasoning,
            "mutation": mutation
        }