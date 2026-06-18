class RuntimeSecurityLayer:

    def validate(self, action):
        blocked = [
            "delete_system32",
            "format_drive"
        ]

        return action not in blocked