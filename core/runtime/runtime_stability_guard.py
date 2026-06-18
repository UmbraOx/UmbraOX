import time


class RuntimeStabilityGuard:
    """
    Prevents unsafe autonomous behavior loops.
    """

    def __init__(self):
        self.last_action_time = 0
        self.cooldown_seconds = 1.0
        self.mode = "safe"  # safe | autonomous

    def allow_action(self):
        now = time.time()

        if self.mode == "safe":
            if now - self.last_action_time < self.cooldown_seconds:
                return False

        self.last_action_time = now
        return True

    def set_mode(self, mode):
        if mode in ("safe", "autonomous"):
            self.mode = mode

    def get_mode(self):
        return self.mode