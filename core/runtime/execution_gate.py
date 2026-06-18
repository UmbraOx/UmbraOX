class ExecutionGate:
    """
    Prevents execution unless proposals are approved.
    """

    def __init__(self, approval_store):
        self.approval_store = approval_store

    def can_execute(self, proposal_id: str) -> bool:
        return self.approval_store.is_approved(proposal_id)