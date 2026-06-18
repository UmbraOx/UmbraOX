class RuntimeGovernor:

    def authorize(self, objective):

        restricted = [
            "delete system32",
            "wipe drive",
            "disable security"
        ]

        lowered = objective.lower()

        for item in restricted:

            if item in lowered:
                return False

        return True