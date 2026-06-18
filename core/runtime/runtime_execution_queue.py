class RuntimeExecutionQueue:

    def __init__(self):
        self.execution = []

    def add(self, task):
        self.execution.append(task)

    def next(self):
        if not self.execution:
            return None

        return self.execution.pop(0)