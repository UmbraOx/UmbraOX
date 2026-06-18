from core.runtime.runtime_kernel import (
    RuntimeKernel
)

from core.runtime.runtime_live_state import (
    RuntimeLiveState
)

from core.runtime.runtime_autonomous_orchestrator import (
    RuntimeAutonomousOrchestrator
)


class RuntimeSystemManager:

    def __init__(self):

        self.kernel = RuntimeKernel()

        self.state = RuntimeLiveState()

        self.orchestrator = (
            RuntimeAutonomousOrchestrator()
        )

        self.kernel.boot()

    def execute(self, objective):

        self.state.update(
            "objective",
            objective
        )

        self.state.update(
            "status",
            "executing"
        )

        result = (
            self.orchestrator
            .orchestrate(objective)
        )

        self.state.update(
            "generated",
            result["generated"]
        )

        self.state.update(
            "tasks",
            result["execution"]
        )

        self.state.update(
            "agents",
            result["execution"]["agents"]
        )

        self.state.update(
            "status",
            "completed"
        )

        return {
            "result": result,
            "state":
            self.state.snapshot()
        }