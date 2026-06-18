class RuntimeSecurityGuard:

    def authorize(
        self,
        action
    ):
        blocked = [
            "delete_os",
            "wipe_drive",
            "format_disk"
        ]

        return action not in blocked