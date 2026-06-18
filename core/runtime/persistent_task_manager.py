class PersistentTaskManager:

    def __init__(self):

        self.tasks = []

    def add_task(self, task):

        self.tasks.append(task)

    def list_tasks(self):

        return self.tasks