from core.runtime.runtime_agent_factory import RuntimeAgentFactory
from core.runtime.runtime_agent_registry import RuntimeAgentRegistry


class RuntimeAgentOrchestrator:
    def __init__(self):
        self.factory = RuntimeAgentFactory()
        self.registry = RuntimeAgentRegistry()

    def initialize(self):
        agents = self.factory.create_agents()

        for agent in agents:
            self.registry.register(agent.name, agent.role)

        return agents

    def registry_snapshot(self):
        return self.registry.all()

    def execute_all(self, objective):
        results = []
        agents = self.factory.create_agents()

        for agent in agents:
            results.append(agent.execute(objective))

        return results