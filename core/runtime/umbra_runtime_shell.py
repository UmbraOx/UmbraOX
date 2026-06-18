class UmbraRuntimeShell:

    def execute(
        self,
        command
    ):
        return {
            "command": command,
            "executed": True
        }