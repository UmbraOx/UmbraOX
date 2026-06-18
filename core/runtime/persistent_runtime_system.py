from core.runtime.runtime_orchestrator import (
    RuntimeOrchestrator
)


class PersistentRuntimeSystem:

    def __init__(self):

        self.runtime = (
            RuntimeOrchestrator()
        )

    def boot(self):

        return self.runtime.initialize()

    def run(self, execution):

        execution_batches = (
            execution.get(
                "execution",
                []
            )
        )

        return self.runtime.execute(
            execution_batches
        )