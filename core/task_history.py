class TaskHistory:

    def __init__(self):
        self.items = []

    def record(self, plan, result):
        self.items.append({
            "plan": plan,
            "result": result
        })