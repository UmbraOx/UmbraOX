class RuntimeExecutionSandbox:
    """
    Lightweight safety filter for runtime execution.
    Blocks dangerous operations and uncontrolled system access.
    """

    DANGEROUS_PATTERNS = [
        "os.system",
        "subprocess",
        "eval(",
        "exec(",
        "open('C:\\\\",
        "rm -rf",
        "del /"
    ]

    def safe(self, objective: str):
        if not objective:
            return False

        lowered = objective.lower()

        for pattern in self.DANGEROUS_PATTERNS:
            if pattern.lower() in lowered:
                return False

        return True