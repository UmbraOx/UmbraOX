class RuntimeLiveState:

    def __init__(self):

        self.state = {
            "objective": None,
            "status": "idle",
            "agents": [],
            "tasks": [],
            "generated": []
        }

    def update(self, key, value):

        self.state[key] = value

    def snapshot(self):

        return self.state