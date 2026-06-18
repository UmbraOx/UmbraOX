import json
import os


class ActiveTasks:
    def __init__(self, path="active_tasks.json"):
        self.path = path

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump([], f)

    def load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def save(self, tasks):
        with open(self.path, "w") as f:
            json.dump(tasks, f, indent=2)

    def add(self, task):
        tasks = self.load()
        tasks.append(task)
        self.save(tasks)
        print(f"[ACTIVE_TASKS] added: {task}")

    def remove(self, task):
        tasks = self.load()

        if task in tasks:
            tasks.remove(task)

        self.save(tasks)
        print(f"[ACTIVE_TASKS] removed: {task}")