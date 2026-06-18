class RuntimePluginManager:

    def __init__(self):

        self.plugins = {}

    def load(
        self,
        plugin
    ):

        result = (
            plugin.initialize()
        )

        self.plugins[
            plugin.name
        ] = plugin

        return result

    def get_plugins(self):

        return list(
            self.plugins.keys()
        )