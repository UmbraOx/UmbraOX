from core.plugin_registry import PluginRegistry


class ToolExecutor:

    def __init__(self):

        self.registry = PluginRegistry()

    # -------------------------------------------------
    # MAIN ENTRY
    # -------------------------------------------------
    def execute(self, tool: dict):

        action = tool.get("action")

        # ---------------------------------------------
        # PLUGIN ROUTING
        # ---------------------------------------------
        if action == "plugin":

            plugin_name = tool.get("name")
            args = tool.get("args", {})

            return self.registry.run(plugin_name, **args)

        return {
            "error": "tool_not_found",
            "action": action
        }