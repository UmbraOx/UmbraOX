class ConstructionStateEngine:

    def __init__(self):

        self.state = "idle"

    def set_state(
        self,
        state
    ):

        self.state = state

    def current(self):

        return self.state