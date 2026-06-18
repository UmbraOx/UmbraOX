from core.runtime.umbra_multi_agent_director import (
    UmbraMultiAgentDirector
)

from core.runtime.umbra_autonomous_execution_cycle import (
    UmbraAutonomousExecutionCycle
)


class UmbraAutonomousCompany:

    def __init__(self):
        self.director = (
            UmbraMultiAgentDirector()
        )

        self.execution = (
            UmbraAutonomousExecutionCycle()
        )

    def operate(
        self,
        objective
    ):
        agents = (
            self.director.direct(
                objective
            )
        )

        execution = (
            self.execution.cycle(
                objective
            )
        )

        return {
            "agents": agents,
            "execution": execution
        }