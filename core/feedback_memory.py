class FeedbackMemory:

    def __init__(self):
        self.history = []

    def record(self, task, result):
        self.history.append({
            "task": task,
            "result": result
        })

    def last(self):
        if not self.history:
            return None
        return self.history[-1]

    def get_all(self):
        return self.history