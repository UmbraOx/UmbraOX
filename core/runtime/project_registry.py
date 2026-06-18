import os

class ProjectRegistry:
    def __init__(self):
        self.projects = {}
        self.path = "projects.json"

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                f.write("{}")

    def register(self, name):
        self.projects[name] = {"name": name}
        return self.projects[name]