class ExecutionHistory:

    def __init__(self):

        self.entries = []

    def add(
        self,
        entry
    ):

        self.entries.append(entry)

    def recent(self):

        return self.entries[-10:]