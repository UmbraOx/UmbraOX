import uuid
from datetime import datetime


class TaskStatus:
    QUEUED = "queued"
    PLANNING = "planning"
    EXECUTING = "executing"
    RETRYING = "retrying"
    FAILED = "failed"
    COMPLETED = "completed"


class Task:

    def __init__(self, description, project="default"):

        self.id = str(uuid.uuid4())

        self.description = description

        self.project = project

        self.status = TaskStatus.QUEUED

        self.created_at = datetime.now()

        self.updated_at = datetime.now()

        self.retries = 0

        self.max_retries = 3

        self.dependencies = []

        self.result = None

        self.error = None

    def set_status(self, status):

        self.status = status

        self.updated_at = datetime.now()


class TaskManager:

    def __init__(self):

        self.tasks = {}

    def create_task(self, description, project="default"):

        task = Task(description, project)

        self.tasks[task.id] = task

        return task

    def get_task(self, task_id):

        return self.tasks.get(task_id)

    def update_task(self, task_id, status):

        task = self.get_task(task_id)

        if task:

            task.set_status(status)

    def all_tasks(self):

        return list(self.tasks.values())