from core.runtime.runtime_execution_orchestrator import (
    RuntimeExecutionOrchestrator
)

from core.runtime.construction_governor import (
    ConstructionGovernor
)


class AutonomousExecutionSystem:

    def __init__(self):

        self.orchestrator = (
            RuntimeExecutionOrchestrator()
        )

        self.governor = (
            ConstructionGovernor()
        )

    def prepare(self, proposals):

        execution = (
            self.orchestrator.orchestrate(
                proposals
            )
        )

        validation = (
            self.governor.validate(
                execution
            )
        )

        return {
            "execution": execution,
            "validation": validation
        }