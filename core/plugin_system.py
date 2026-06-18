import importlib
import os


class PluginSystem:

    def __init__(self, plugin_registry):

        self.registry = plugin_registry

    def load_plugins(self):

        plugin_dir = "core/plugins"

        if not os.path.exists(plugin_dir):
            return

        for file in os.listdir(plugin_dir):

            if not file.endswith(".py"):
                continue

            if file.startswith("_"):
                continue

            module_name = file[:-3]

            module_path = f"core.plugins.{module_name}"

            try:

                module = importlib.import_module(module_path)

                if hasattr(module, "Plugin"):

                    plugin = module.Plugin()

                    self.registry.register(module_name, plugin)

                    print(f"[PLUGIN] Loaded: {module_name}")

            except Exception as e:

                print(f"[PLUGIN] Failed loading {module_name}: {e}")