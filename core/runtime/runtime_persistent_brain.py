from pathlib import Path

import json


class RuntimePersistentBrain:

    def __init__(self):

        self.memory_path = Path(
            "runtime_memory.json"
        )

        if not self.memory_path.exists():

            with open(
                self.memory_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump([], file)

    def load(self):

        try:

            with open(
                self.memory_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return []

    def remember(
        self,
        item
    ):

        memory = self.load()

        memory.append(item)

        with open(
            self.memory_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                memory,
                file,
                indent=4
            )

    def clear(self):

        with open(
            self.memory_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump([], file)