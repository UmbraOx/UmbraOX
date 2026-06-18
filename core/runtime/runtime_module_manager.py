class RuntimeModuleManager:
    def __init__(self):
        self.modules = []

    def register(self, module):
        self.modules.append(module)

    def list_modules(self):
        return self.modules