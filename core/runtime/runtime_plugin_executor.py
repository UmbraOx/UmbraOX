class RuntimePluginExecutor:

    def execute(
        self,
        plugin,
        payload
    ):
        return plugin.execute(
            payload
        )