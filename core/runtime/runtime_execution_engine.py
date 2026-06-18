from core.runtime.runtime_agent_orchestrator import RuntimeAgentOrchestrator
from core.runtime.runtime_execution_monitor import RuntimeExecutionMonitor
from core.runtime.runtime_failure_recovery import RuntimeFailureRecovery


class RuntimeExecutionEngine:

    def __init__(self):
        self.orchestrator = RuntimeAgentOrchestrator()
        self.monitor = RuntimeExecutionMonitor()
        self.recovery = RuntimeFailureRecovery()

    def execute(self, graph):

        try:
            agents = self.orchestrator.initialize()

            results = []

            for agent, node in zip(agents, graph["children"]):
                result = agent.execute(node["objective"])
                results.append(result)

            metrics = self.monitor.track(results)

            return {
                "run_id": graph.get("objective", "unknown"),
                "results": results,
                "metrics": metrics,
                "agents": self.orchestrator.registry_snapshot()
            }

        except Exception as e:
            return self.recovery.recover(e)