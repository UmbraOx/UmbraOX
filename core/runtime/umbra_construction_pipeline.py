from core.runtime.runtime_safe_executor import (
    RuntimeSafeExecutor
)

from core.runtime.runtime_autonomous_core import (
    RuntimeAutonomousCore
)


class UmbraConstructionPipeline:

    def __init__(self):

        self.executor = (
            RuntimeSafeExecutor()
        )

        self.core = (
            RuntimeAutonomousCore()
        )

    def build(
        self,
        phases
    ):

        results = []

        for phase in phases:

            execution = (
                self.core.execute(
                    phase["objective"]
                )
            )

            generation = (
                self.executor.execute(
                    phase["objective"]
                )
            )

            results.append({
                "phase": phase,
                "execution": execution,
                "generation": generation
            })

        return results