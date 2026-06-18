from __future__ import annotations

from datetime import datetime


class RuntimePromptSession:

    def __init__(self):
        self.history = []

    def submit(
        self,
        prompt: str,
    ):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
        }

        self.history.append(entry)

        return entry

    def load(self):
        return self.history