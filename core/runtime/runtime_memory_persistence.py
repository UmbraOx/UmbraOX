from __future__ import annotations

import json
from pathlib import Path


class RuntimeMemoryPersistence:
    def __init__(self, path: str = "runtime_memory.json"):
        self.path = Path(path)

    def save_memory(self, memory: dict):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(memory, file, indent=2)

    def load_memory(self):
        if not self.path.exists():
            return {}

        with open(self.path, "r", encoding="utf-8") as file:
            return json.load(file)