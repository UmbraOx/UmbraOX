class TaskGraph:

    def __init__(self):
        self.nodes = []

    def add_task(self, task: dict):
        task.setdefault("status", "pending")
        self.nodes.append(task)

    def get_pending(self):
        return [n for n in self.nodes if n["status"] == "pending"]

    def mark_done(self, node):
        node["status"] = "done"