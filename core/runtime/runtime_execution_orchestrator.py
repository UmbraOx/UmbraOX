from core.runtime.execution_planner import (
    ExecutionPlanner
)


class RuntimeExecutionOrchestrator:

    def __init__(self):

        self.planner = (
            ExecutionPlanner()
        )

    def orchestrate(self, proposals):

        execution_batches = []

        for proposal in proposals:

            execution = (
                self.planner.plan(
                    proposal
                )
            )

            execution_batches.append({
                "proposal": proposal,
                "execution": execution
            })

        return execution_batches