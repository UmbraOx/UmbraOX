class RuntimeSafetyGuard:

    BLOCKED = [
        "format",
        "shutdown",
        "delete system32"
    ]

    def allowed(self, objective):

        lowered = objective.lower()

        for blocked in self.BLOCKED:

            if blocked in lowered:
                return False

        return True