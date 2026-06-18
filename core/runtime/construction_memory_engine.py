class ConstructionMemoryEngine:

    def __init__(self):

        self.memory = []

    def record_phase(
        self,
        phase
    ):

        self.memory.append(phase)

    def phases(self):

        return self.memory