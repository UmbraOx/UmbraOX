from core.runtime.implementation_engine import ImplementationEngine
from core.runtime.service_scaffolder import ServiceScaffolder
from core.runtime.agent_factory import AgentFactory


class AutonomousBuilder:

    def __init__(self):

        self.implementation_engine = (
            ImplementationEngine()
        )

        self.service_scaffolder = (
            ServiceScaffolder()
        )

        self.agent_factory = (
            AgentFactory()
        )

    def build(self, proposal):

        implementation = (
            self.implementation_engine.create(
                proposal
            )
        )

        services = (
            self.service_scaffolder.scaffold(
                proposal
            )
        )

        agents = (
            self.agent_factory.generate(
                proposal
            )
        )

        return {
            "proposal": proposal,
            "implementation": implementation,
            "services": services,
            "agents": agents,
            "status": "prepared"
        }