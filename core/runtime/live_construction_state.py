class LiveConstructionState:

    def __init__(self):
        self.state = {
            "active": [],
            "completed": [],
            "failed": []
        }

    def start(self, task):
        self.state["active"].append(task)

    def complete(self, task):
        if task in self.state["active"]:
            self.state["active"].remove(task)

        self.state["completed"].append(task)

    def fail(self, task):
        self.state["failed"].append(task)

    def snapshot(self):
        return self.state