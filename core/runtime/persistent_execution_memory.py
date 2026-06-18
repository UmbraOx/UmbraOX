import json
import os


class PersistentExecutionMemory:

    def __init__(self):

        self.path = (
            "memory/execution_memory.json"
        )

        os.makedirs(
            "memory",
            exist_ok=True
        )

        if not os.path.exists(
            self.path
        ):

            with open(
                self.path,
                "w"
            ) as file:

                json.dump([], file)

    def record(
        self,
        entry
    ):

        data = self.load()

        data.append(entry)

        with open(
            self.path,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    def load(self):

        with open(
            self.path,
            "r"
        ) as file:

            return json.load(file)