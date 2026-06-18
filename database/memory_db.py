import json
import os
from core.config import MEMORY_PATH


class MemoryDB:

    def __init__(self):
        os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)

        if not os.path.exists(MEMORY_PATH):
            with open(MEMORY_PATH, "w") as f:
                json.dump([], f)

    def load(self):
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data):
        with open(MEMORY_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def append(self, item):
        data = self.load()
        data.append(item)
        self.save(data)