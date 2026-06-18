class ProjectStateTracker:

    def __init__(self):

        self.state = {}

    def update(
        self,
        key,
        value
    ):

        self.state[key] = value

    def snapshot(self):

        return self.state