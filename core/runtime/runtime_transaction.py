class RuntimeTransaction:

    def __init__(self):

        self.actions = []

    def record(self, action):

        self.actions.append(action)

    def rollback(self):

        reversed_actions = list(
            reversed(self.actions)
        )

        return reversed_actions