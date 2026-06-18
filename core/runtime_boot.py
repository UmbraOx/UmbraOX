from core.tool_registry import ToolRegistry
from core.plugin_registry import PluginRegistry
from core.plugin_system import PluginSystem


class RuntimeBoot:

    def __init__(self):

        self.tool_registry = ToolRegistry()
        self.plugin_registry = PluginRegistry()

        self.plugin_system = PluginSystem(
            self.plugin_registry
        )

    def boot(self):

        print("[RUNTIME] Booting Umbra Runtime")

        self.plugin_system.load_plugins()

        print("[RUNTIME] Runtime Ready")