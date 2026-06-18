import time
import json
import os

class VersionManager:

    def __init__(self, path="versions"):
        self.path = path
        os.makedirs(self.path, exist_ok=True)

    def save_version(self, name, data):
        file = os.path.join(self.path, f"{name}_{int(time.time())}.json")

        with open(file, "w") as f:
            json.dump(data, f, indent=2)

        return file

    def list_versions(self):
        return os.listdir(self.path)


version_manager = VersionManager()