class ExecutionHistoryLog:

    def __init__(self):

        self.history = []

    def record(
        self,
        entry
    ):

        self.history.append(entry)

    def all(self):

        return self.history