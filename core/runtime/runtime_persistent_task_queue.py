import json
import os


class RuntimePersistentTaskQueue:

    def __init__(self):
        self.path = "runtime_tasks.json"

    def push(
        self,
        task
    ):
        tasks = self.load()

        tasks.append(task)

        with open(
            self.path,
            "w"
        ) as f:
            json.dump(
                tasks,
                f,
                indent=4
            )

    def load(self):
        if not os.path.exists(
            self.path
        ):
            return []

        with open(
            self.path,
            "r"
        ) as f:
            return json.load(f)