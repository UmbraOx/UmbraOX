class RuntimeRegistry:
    """
    SINGLE SOURCE OF TRUTH FOR ACTIVE SYSTEM COMPONENTS
    """

    def __init__(self):
        self.components = {}
        self.active_kernel = None

    def register_kernel(self, kernel):
        self.active_kernel = kernel

    def register_component(self, name: str, component):
        if name in self.components:
            raise Exception(f"Duplicate component blocked: {name}")

        self.components[name] = component

    def get(self, name: str):
        return self.components.get(name)

    def list_components(self):
        return list(self.components.keys())