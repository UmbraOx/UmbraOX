class RuntimeToolExecutor:

    def execute(
        self,
        tool,
        *args,
        **kwargs
    ):

        return tool(
            *args,
            **kwargs
        )