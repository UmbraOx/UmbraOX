class AgentStateManager:

    def __init__(self):

        self.states = {}

    def set_state(
        self,
        agent,
        state
    ):

        self.states[agent] = state

    def get_state(
        self,
        agent
    ):

        return self.states.get(
            agent,
            "idle"
        )