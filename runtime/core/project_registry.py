import json
import os
from core.config import BASE_DIR


REGISTRY_FILE = os.path.join(BASE_DIR, "runtime", "registry", "projects.json")


class ProjectRegistry:
    def __init__(self):
        os.makedirs(os.path.dirname(REGISTRY_FILE), exist_ok=True)

        if not os.path.exists(REGISTRY_FILE):
            with open(REGISTRY_FILE, "w") as f:
                json.dump([], f)

    def load(self):
        with open(REGISTRY_FILE, "r") as f:
            return json.load(f)

    def save(self, data):
        with open(REGISTRY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def register_project(self, name):
        projects = self.load()

        projects.append({
            "name": name,
            "status": "active"
        })

        self.save(projects)