class RuntimeCommandCenter:
    """
    Single routing layer for Umbra operations.
    """

    def __init__(self, kernel):
        self.kernel = kernel

    def handle(self, command, payload=None):
        if command == "analyze":
            return self.kernel.run_analysis()

        if command == "improve":
            return self.kernel.run_improvement_cycle()

        if command == "repair":
            return self.kernel.run_repair(payload)

        if command == "pipeline":
            return self.kernel.run_pipeline(payload)

        return {
            "error": "unknown_command",
            "command": command
        }