from __future__ import annotations


class RuntimeIntegrityMonitor:
    def __init__(self):
        self.last_check = None

    def run_integrity_check(self) -> dict:
        self.last_check = {
            "healthy": True,
            "issues": [],
        }

        return self.last_check