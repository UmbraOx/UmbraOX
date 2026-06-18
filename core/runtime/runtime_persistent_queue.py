import json
import os


class RuntimePersistentQueue:

    FILE = "memory/task_queue.json"

    def __init__(self):

        os.makedirs(
            "memory",
            exist_ok=True
        )

    def save(self, tasks):

        with open(self.FILE, "w") as f:

            json.dump(tasks, f, indent=2)

    def load(self):

        try:

            with open(self.FILE, "r") as f:

                return json.load(f)

        except:
            return []