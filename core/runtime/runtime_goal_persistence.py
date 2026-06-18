import json
import os


class RuntimeGoalPersistence:

    def __init__(self):

        self.path = (
            "runtime_memory/goals.json"
        )

        os.makedirs(
            "runtime_memory",
            exist_ok=True
        )

    def save(self, goals):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(goals, file, indent=4)

    def load(self):

        if not os.path.exists(self.path):
            return []

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)