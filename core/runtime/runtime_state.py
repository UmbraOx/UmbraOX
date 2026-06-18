class RuntimeState:

    def __init__(self):
        self.state = {
            "status": "idle",
            "active_objective": None,
            "active_tasks": [],
            "active_agents": [],
            "generated_modules": [],
            "failures": [],
            "memory_loaded": False,
            "runtime_booted": False
        }

    def set(self, key, value):
        self.state[key] = value

    def get(self, key, default=None):
        return self.state.get(key, default)

    def snapshot(self):
        return dict(self.state)