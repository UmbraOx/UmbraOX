class RuntimeConfig:

    def __init__(self):

        self.config = {
            "max_agents": 16,
            "max_execution_depth": 8,
            "safe_mode": True,
            "allow_file_write": True,
            "allow_code_execution": False,
            "memory_path": "memory",
            "generated_path": "generated"
        }

    def get(self, key, default=None):
        return self.config.get(key, default)