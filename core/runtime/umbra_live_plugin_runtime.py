from core.runtime.runtime_plugin_loader import (
    RuntimePluginLoader
)


class UmbraLivePluginRuntime:

    def __init__(self):
        self.loader = (
            RuntimePluginLoader()
        )

    def plugins(self):
        return self.loader.load_plugins()