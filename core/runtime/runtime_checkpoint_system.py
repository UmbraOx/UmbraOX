from copy import deepcopy


class RuntimeCheckpointSystem:
    def __init__(self):
        self.checkpoints = {}

    def create_checkpoint(self, name, state):
        self.checkpoints[name] = deepcopy(state)

    def restore_checkpoint(self, name):
        return deepcopy(self.checkpoints.get(name))

    def list_checkpoints(self):
        return list(self.checkpoints.keys())