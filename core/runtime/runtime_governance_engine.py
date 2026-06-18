from datetime import datetime


class RuntimeGovernanceEngine:
    """
    Controls what Umbra is allowed to change.
    This is the safety gate for self-modification.
    """

    def __init__(self):
        self.approval_log = []

    def evaluate_change_request(self, module, reason):
        risk = self._assess_risk(module, reason)

        decision = {
            "module": module,
            "reason": reason,
            "risk": risk,
            "approved": risk != "high",
            "timestamp": datetime.now().isoformat(),
        }

        self.approval_log.append(decision)
        return decision

    def _assess_risk(self, module, reason):
        if "runtime_execution" in module:
            return "high"

        if "repair" in module:
            return "medium"

        if "test" in module:
            return "low"

        return "low"