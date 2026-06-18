class UmbraRuntimeTerminal:

    def run(
        self,
        command
    ):
        return {
            "terminal_command": command,
            "success": True
        }