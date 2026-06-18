class RuntimeCycleManager:

    def __init__(self):

        self.cycles = 0

    def run_cycle(self):

        self.cycles += 1

        return {
            "cycle": "completed",
            "count": self.cycles
        }