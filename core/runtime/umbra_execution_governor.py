class UmbraExecutionGovernor:

    BLOCKED = [
        "disable antivirus",
        "delete windows",
        "wipe disk",
        "credential theft"
    ]

    def approve(
        self,
        objective
    ):

        lowered = objective.lower()

        for blocked in self.BLOCKED:

            if blocked in lowered:

                return False

        return True