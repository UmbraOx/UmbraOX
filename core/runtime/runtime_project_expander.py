from core.runtime.autonomous_builder import (
    AutonomousBuilder
)


class RuntimeProjectExpander:

    def __init__(self):

        self.builder = AutonomousBuilder()

    def expand(self, proposals):

        expansions = []

        for proposal in proposals:

            result = self.builder.build(
                proposal
            )

            expansions.append(result)

        return expansions