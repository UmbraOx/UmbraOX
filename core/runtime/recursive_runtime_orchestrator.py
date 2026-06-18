from core.runtime.autonomous_construction_runtime import (
    AutonomousConstructionRuntime
)


class RecursiveRuntimeOrchestrator:

    def __init__(self):

        self.runtime = (
            AutonomousConstructionRuntime()
        )

    def orchestrate(
        self,
        objective
    ):

        return self.runtime.build(
            objective
        )