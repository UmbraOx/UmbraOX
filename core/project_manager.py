from core.project_memory import ProjectMemory


class ProjectManager:

    def __init__(self):

        self.memory = ProjectMemory()

    def set_active_project(self, name):

        self.memory.update_project(
            name,
            {
                "active": True
            }
        )

    def update_status(self, name, status):

        self.memory.update_project(
            name,
            {
                "status": status
            }
        )

    def get_project(self, name):

        return self.memory.get_project(name)