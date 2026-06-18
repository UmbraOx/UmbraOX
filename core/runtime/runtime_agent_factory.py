from core.runtime.runtime_worker_agent import RuntimeWorkerAgent


class RuntimeAgentFactory:
    """
    Creates runtime worker agents.
    """

    def create_agents(self):
        return [
            RuntimeWorkerAgent("builder", "code_builder"),
            RuntimeWorkerAgent("tester", "code_tester"),
            RuntimeWorkerAgent("analyzer", "system_analyzer"),
            RuntimeWorkerAgent("executor", "task_executor"),
        ]

    def create_agent(self, name, role):
        return RuntimeWorkerAgent(name, role)