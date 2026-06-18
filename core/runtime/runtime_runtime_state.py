import json
from pathlib import Path


class RuntimeState:

    def __init__(
        self,
        state_file="runtime_state.json"
    ):

        self.state_file = Path(
            state_file
        )

        self.state = self.load()

    def load(self):

        if not self.state_file.exists():

            return {
                "boot_count": 0,
                "last_tasks": [],
                "last_status": "offline"
            }

        try:

            with open(
                self.state_file,
                "r",
                encoding="utf-8"
            ) as f:

                return json.load(f)

        except Exception:

            return {
                "boot_count": 0,
                "last_tasks": [],
                "last_status": "corrupted"
            }

    def save(self):

        with open(
            self.state_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.state,
                f,
                indent=4
            )

    def set_status(
        self,
        status
    ):

        self.state["last_status"] = status

        self.save()

    def increment_boot_count(self):

        self.state["boot_count"] += 1

        self.save()

    def record_task(
        self,
        task
    ):

        self.state["last_tasks"].append(
            task
        )

        self.state["last_tasks"] = (
            self.state["last_tasks"][-25:]
        )

        self.save()

    def get_state(self):

        return self.state