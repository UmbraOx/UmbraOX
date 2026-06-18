class ApprovalStore:
    """
    Stores proposal approvals and rejections.
    """

    def __init__(self):
        self.approved = set()
        self.rejected = set()

    def approve(self, proposal_id: str):
        self.approved.add(proposal_id)

    def reject(self, proposal_id: str):
        self.rejected.add(proposal_id)

    def is_approved(self, proposal_id: str) -> bool:
        return proposal_id in self.approved

    def is_rejected(self, proposal_id: str) -> bool:
        return proposal_id in self.rejected


approval_store = ApprovalStore()