class ToolRegistry:
    """
    Central registry for tools.
    Safe default version: always usable without injection.
    """

    def __init__(self):
        self.tools = {}

    def register(self, name: str, fn):
        self.tools[name] = fn

    def get(self, name: str):
        return self.tools.get(name)

    def list_tools(self):
        return list(self.tools.keys())