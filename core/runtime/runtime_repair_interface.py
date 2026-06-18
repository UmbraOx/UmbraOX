from typing import Any, Dict


class RuntimeRepairInterface:
    """
    Unified repair entry point.
    Replaces fragmented repair systems.
    """

    def __init__(self, failure_memory=None):
        self.failure_memory = failure_memory

    def repair(self, error: Exception) -> Dict[str, Any]:
        error_name = type(error).__name__

        if self.failure_memory:
            try:
                self.failure_memory.record("repair", str(error))
            except Exception:
                pass

        return {
            "status": "repair_logged",
            "error_type": error_name,
        }

    def plan_fix(self, error: Exception) -> Dict[str, Any]:
        return {
            "plan": "safe_noop_fix",
            "reason": str(error),
        }

    def apply_fix(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "applied_stub_fix",
            "plan": plan,
        }