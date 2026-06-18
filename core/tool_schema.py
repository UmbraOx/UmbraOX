class ToolSchema:

    @staticmethod
    def format(tool: str, action: str, path: str = None, content: str = None):

        return {
            "tool": tool,
            "action": action,
            "path": path,
            "content": content
        }