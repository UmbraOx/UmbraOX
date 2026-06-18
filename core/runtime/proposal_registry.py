class ProposalRegistry:
    """
    Stores active proposals in memory for CLI interaction.
    """

    def __init__(self):
        self.proposals = {}

    def add_batch(self, batch):
        for item in batch:
            self.proposals[item["id"]] = item

    def get(self, proposal_id: str):
        return self.proposals.get(proposal_id)

    def list_all(self):
        return list(self.proposals.values())