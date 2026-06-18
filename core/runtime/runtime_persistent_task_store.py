from __future__ import annotations

import json
from pathlib import Path


class RuntimePersistentTaskStore:
    def __init__(self, storage_path: str = "runtime_tasks.json"):
        self.storage_path = Path(storage_path)
        self.tasks: list[dict] = []

        if self.storage_path.exists():
            self.load_tasks()

    def add_task(self, task: dict):
        self.tasks.append(task)
        self.save_tasks()

    def save_tasks(self):
        with open(self.storage_path, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=2)

    def load_tasks(self):
        with open(self.storage_path, "r", encoding="utf-8") as file:
            self.tasks = json.load(file)

    def get_tasks(self):
        return self.tasks