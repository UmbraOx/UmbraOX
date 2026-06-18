import json
import os
import time

class SnapshotManager:
    """
    Handles safe state snapshots for rollback + recovery.
    """

    def __init__(self, path="snapshots"):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def save(self, name: str, data: dict):
        file_path = os.path.join(self.path, f"{name}.json")

        snapshot = {
            "timestamp": time.time(),
            "name": name,
            "data": data
        }

        with open(file_path, "w") as f:
            json.dump(snapshot, f, indent=2)

        return file_path

    def load(self, name: str):
        file_path = os.path.join(self.path, f"{name}.json")

        if not os.path.exists(file_path):
            return None

        with open(file_path, "r") as f:
            return json.load(f)

    def list_snapshots(self):
        return os.listdir(self.path)