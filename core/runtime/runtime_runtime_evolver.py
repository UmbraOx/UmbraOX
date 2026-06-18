class RuntimeRuntimeEvolver:
    def evolve(self, runtime_state):
        runtime_state["version"] += 1
        runtime_state["evolved"] = True
        return runtime_state