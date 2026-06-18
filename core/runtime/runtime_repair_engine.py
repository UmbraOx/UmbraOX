from core.runtime.self_repair import SelfRepairSystem


class RuntimeRepairEngine:
    """
    Compatibility wrapper around SelfRepairSystem.
    """

    def __init__(self, failure_memory=None):
        self.inner = SelfRepairSystem(failure_memory)

    def repair(self, error):
        return self.inner.repair(error)

    def attempt_fix(self, error):
        return self.inner.attempt_fix(error)