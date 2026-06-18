class ProjectGraph:

    def __init__(self):
        self.projects = {}

    def add(self, project_name, node):
        self.projects.setdefault(project_name, []).append(node)

    def get(self, project_name):
        return self.projects.get(project_name, [])