class PluginRegistry:

    def __init__(self):
        self.plugins = {}

    def register(self, plugin_name, plugin_object):

        self.plugins[plugin_name] = plugin_object

    def get(self, plugin_name):

        return self.plugins.get(plugin_name)

    def list_plugins(self):

        return list(self.plugins.keys())