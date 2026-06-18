class ToolRouter:
    """
    Converts input → structured execution plan
    """

    def __init__(self, registry):
        self.registry = registry

    def route(self, user_input: str):
        # minimal stable planner (no AI dependency yet)
        return {
            "steps": [
                {
                    "tool": "fs.create_from_prompt",
                    "args": {"input": user_input}
                }
            ]
        }