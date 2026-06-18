class SelfRepairSystem:
    """
    Compatibility wrapper around RuntimeSelfRepairEngine.
    """

    def __init__(self, failure_memory):
        self.failure_memory = failure_memory
        self.engine = None

    def attach_engine(self, engine):
        self.engine = engine

    def attempt_fix(self, error):
        if self.engine:
            return self.engine.repair(error)

        error_name = type(error).__name__

        self.failure_memory.record(
            "self_repair",
            str(error)
        )

        return {
            "status": "repair_attempted",
            "error": error_name
        }

    def repair(self, error):
        return self.attempt_fix(error)