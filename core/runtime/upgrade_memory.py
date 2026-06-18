class UpgradeMemory:
    """
    Tracks accepted/declined upgrades so Umbra doesn't spam them.
    """

    def __init__(self):
        self.approved = set()
        self.rejected = set()

    def approve(self, proposal_id: str):
        self.approved.add(proposal_id)
        self.rejected.discard(proposal_id)

    def reject(self, proposal_id: str):
        self.rejected.add(proposal_id)
        self.approved.discard(proposal_id)

    def is_rejected(self, proposal_id: str) -> bool:
        return proposal_id in self.rejected

    def is_approved(self, proposal_id: str) -> bool:
        return proposal_id in self.approved