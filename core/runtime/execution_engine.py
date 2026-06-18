class ExecutionEngine:
    """
    Executes approved proposals safely.
    """

    def __init__(self, tool_registry):
        self.tool_registry = tool_registry

    def execute(self, proposal: dict):
        tool = proposal.get("target")

        if not tool:
            return {"status": "failed", "reason": "no target"}

        # safe execution abstraction
        if hasattr(self.tool_registry, tool):
            action = getattr(self.tool_registry, tool)
            return action(proposal)

        return {"status": "failed", "reason": f"tool not found: {tool}"}