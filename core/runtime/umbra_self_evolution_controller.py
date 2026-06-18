import time


class UmbraSelfEvolutionController:
    """
    Controls whether Umbra is allowed to self-improve.

    This is NOT autonomous editing.
    This is a gated evolution scheduler.
    """

    def __init__(self, cooldown_cycles: int = 5):
        self.cooldown_cycles = cooldown_cycles
        self.last_evolution_cycle = 0
        self.evolution_enabled = True

    def can_evolve(self, current_cycle: int) -> bool:
        if not self.evolution_enabled:
            return False

        return (current_cycle - self.last_evolution_cycle) >= self.cooldown_cycles

    def mark_evolved(self, current_cycle: int):
        self.last_evolution_cycle = current_cycle