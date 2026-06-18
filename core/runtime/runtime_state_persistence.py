import json
import os


class RuntimeStatePersistence:

    def __init__(self):
        self.path = "runtime_state.json"

    def save(
        self,
        state
    ):
        with open(
            self.path,
            "w"
        ) as f:
            json.dump(
                state,
                f,
                indent=4
            )

    def load(self):
        if not os.path.exists(
            self.path
        ):
            return {}

        with open(
            self.path,
            "r"
        ) as f:
            return json.load(f)