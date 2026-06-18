# core/runtime/snapshot_system.py

import json
import os
import time


class SnapshotSystem:

    def __init__(self, directory="snapshots"):

        self.directory = directory

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def save(self, name, data):

        timestamp = int(time.time())

        snapshot = {
            "timestamp": timestamp,
            "name": name,
            "data": data
        }

        path = os.path.join(
            self.directory,
            f"{name}.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)

        print(f"[SNAPSHOT] saved: {name}")

    def load(self, name):

        path = os.path.join(
            self.directory,
            f"{name}.json"
        )

        if not os.path.exists(path):
            return None

        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_snapshots(self):

        return os.listdir(self.directory)