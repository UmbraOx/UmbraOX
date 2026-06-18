class RuntimeAgentDispatcher:
    def __init__(self):
        self.dispatch_history = []

    def dispatch(self, task):
        result = {
            "task": task,
            "agent": "default_agent",
            "status": "assigned"
        }

        self.dispatch_history.append(result)

        return result