class UmbraLiveShell:

    def execute(
        self,
        command
    ):
        return {
            "command": command,
            "status": "executed"
        }