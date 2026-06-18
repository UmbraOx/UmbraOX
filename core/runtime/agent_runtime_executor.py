from core.runtime.recursive_execution_engine import (
    RecursiveExecutionEngine
)


class AgentRuntimeExecutor:

    def __init__(self):

        self.engine = (
            RecursiveExecutionEngine()
        )

    def execute(
        self,
        objectives
    ):

        return self.engine.execute(
            objectives
        )