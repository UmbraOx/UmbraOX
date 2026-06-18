from core.runtime.runtime_plugin_loader import (
    RuntimePluginLoader
)


class UmbraPluginManager:

    def __init__(self):
        self.loader = (
            RuntimePluginLoader()
        )

    def load(self):
        return self.loader.load_plugins()