from core.runtime.execution_gate import ExecutionGate
from core.runtime.approval_store import approval_store


class Executor:

    def __init__(self, registry):
        self.registry = registry
        self.gate = ExecutionGate(approval_store)

    def execute(self, tool_name, args=None):

        if args is None:
            args = {}

        tool = self.registry.get(tool_name)

        if tool is None:
            raise Exception(f"Tool not found: {tool_name}")

        return tool(**args)