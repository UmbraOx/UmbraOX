from __future__ import annotations


class RuntimeProjectRegistry:
    def __init__(self):
        self.projects: dict[str, dict] = {}

    def register_project(self, name: str, metadata: dict):
        self.projects[name] = metadata

    def get_project(self, name: str):
        return self.projects.get(name)

    def list_projects(self):
        return list(self.projects.keys())