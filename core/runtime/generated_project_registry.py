class GeneratedProjectRegistry:

    def __init__(self):

        self.projects = []

    def register(
        self,
        project
    ):

        self.projects.append(project)

    def all(self):

        return self.projects