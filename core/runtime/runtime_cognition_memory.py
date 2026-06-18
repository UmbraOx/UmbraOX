class RuntimeCognitionMemory:

    def __init__(self):

        self.thoughts = []

    def think(self, thought):

        self.thoughts.append(
            thought
        )

    def history(self):

        return self.thoughts