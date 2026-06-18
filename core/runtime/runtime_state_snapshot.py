class RuntimeStateSnapshot:

    def snapshot(self, state):
        return {
            "snapshot": state,
            "saved": True
        }