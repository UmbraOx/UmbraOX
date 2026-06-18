class RuntimeCapabilityRegistry:
    def __init__(self):
        self.capabilities = {}

    def register(self, name, capability):
        self.capabilities[name] = capability

    def get(self, name):
        return self.capabilities.get(name)

    def get_capabilities(self):
        return self.capabilities