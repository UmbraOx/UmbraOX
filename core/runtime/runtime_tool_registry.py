class RuntimeToolRegistry:

    def __init__(self):

        self.tools = {}

    def register(
        self,
        name,
        tool
    ):

        self.tools[name] = tool

    def get_tool(
        self,
        name
    ):

        return self.tools.get(name)