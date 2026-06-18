from __future__ import annotations


class RuntimeMasterLoop:
    def __init__(self):
        self.cycles = 0

    def run_cycle(self):
        self.cycles += 1

        return {
            "cycle": self.cycles,
            "success": True,
        }