class RuntimeFailSafe:

    def recover(self, error):

        return {
            "recovered": True,
            "error": str(error),
            "action": "rollback_snapshot"
        }