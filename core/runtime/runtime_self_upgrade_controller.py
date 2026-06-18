class RuntimeSelfUpgradeController:
    """
    Handles upgrade proposals from improvement loop.
    Does NOT apply changes directly.
    """

    def __init__(self, governance_engine):
        self.governance = governance_engine
        self.pending_upgrades = []

    def propose_upgrade(self, module, reason):
        decision = self.governance.evaluate_change_request(module, reason)

        proposal = {
            "module": module,
            "reason": reason,
            "approved": decision["approved"],
            "risk": decision["risk"],
        }

        self.pending_upgrades.append(proposal)
        return proposal

    def get_pending(self):
        return self.pending_upgrades

    def clear(self):
        self.pending_upgrades = []