class SelfRepairSystem:
    """
    Minimal safe self-repair layer.
    """

    def __init__(self, failure_memory=None):
        self.failure_memory = failure_memory

    def attempt_fix(self, error):
        error_name = type(error).__name__

        if self.failure_memory:
            try:
                self.failure_memory.record("self_repair", str(error))
            except Exception:
                pass

        return {
            "status": "repair_attempted",
            "error": error_name,
        }

    def repair(self, error):
        return self.attempt_fix(error)