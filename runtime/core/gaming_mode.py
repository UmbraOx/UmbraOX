# core/runtime/gaming_mode.py

class GamingModeController:
    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def is_throttled(self):
        return self.enabled