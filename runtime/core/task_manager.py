import json
import os
from datetime import datetime
from core.config import TASKS_PATH


class TaskManager:
    def __init__(self):
        os.makedirs(TASKS_PATH, exist_ok=True)
        self.task_file = os.path.join(TASKS_PATH, "tasks.json")

        if not os.path.exists(self.task_file):
            with open(self.task_file, "w") as f:
                json.dump([], f)

    def add_task(self, task: dict):
        task["created_at"] = str(datetime.utcnow())
        task["status"] = "pending"

        tasks = self.load_tasks()
        tasks.append(task)

        self.save_tasks(tasks)

    def load_tasks(self):
        with open(self.task_file, "r") as f:
            return json.load(f)

    def save_tasks(self, tasks):
        with open(self.task_file, "w") as f:
            json.dump(tasks, f, indent=2)

    def get_pending(self):
        return [t for t in self.load_tasks() if t["status"] == "pending"]