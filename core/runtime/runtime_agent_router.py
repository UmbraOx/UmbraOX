class RuntimeAgentRouter:

    def __init__(self):

        self.routes = {}

    def route(
        self,
        agent,
        task
    ):

        self.routes[agent] = task

        return {
            "agent": agent,
            "task": task,
            "status": "routed"
        }