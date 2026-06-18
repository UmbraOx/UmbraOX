from __future__ import annotations


class RuntimeStateRecovery:
    def __init__(self):
        self.last_state = None

    def save_state(self, state: dict):
        self.last_state = state

    def recover_state(self):
        return self.last_state