from __future__ import annotations


class RuntimeProjectMemory:
    def __init__(self):
        self.memory: dict[str, list] = {}

    def store(self, project: str, item: dict):
        self.memory.setdefault(project, []).append(item)

    def recall(self, project: str):
        return self.memory.get(project, [])