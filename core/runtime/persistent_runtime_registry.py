class PersistentRuntimeRegistry:

    def __init__(self):

        self.registry = {}

    def register(
        self,
        runtime,
        state
    ):

        self.registry[runtime] = state

    def all(self):

        return self.registry