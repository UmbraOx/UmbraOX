class GovernanceState:
    """
    Tracks governance states
    for proposals.
    """

    def __init__(self):

        self.states = {}

    def set_state(self, proposal_id, state):

        self.states[proposal_id] = state

    def get_state(self, proposal_id):

        return self.states.get(
            proposal_id,
            "pending"
        )