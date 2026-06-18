from core.runtime.runtime_objective_graph import (
    RuntimeObjectiveGraph
)

from core.runtime.runtime_execution_engine import (
    RuntimeExecutionEngine
)

from core.runtime.runtime_generation_pipeline import (
    RuntimeGenerationPipeline
)

from core.runtime.runtime_execution_history import (
    RuntimeExecutionHistory
)


class RuntimeAutonomousOrchestrator:

    def __init__(self):

        self.graph = (
            RuntimeObjectiveGraph()
        )

        self.execution = (
            RuntimeExecutionEngine()
        )

        self.pipeline = (
            RuntimeGenerationPipeline()
        )

        self.history = (
            RuntimeExecutionHistory()
        )

    def orchestrate(self, objective):

        graph = self.graph.build(
            objective
        )

        generated = (
            self.pipeline.generate([
                "runtime",
                "agents",
                "memory",
                "deployment",
                "ui"
            ])
        )

        execution = (
            self.execution.execute(graph)
        )

        payload = {
            "objective": objective,
            "graph": graph,
            "generated": generated,
            "execution": execution
        }

        self.history.record(payload)

        return payload