class RuntimeCapabilityInjector:

    def __init__(self):

        self.capabilities = {}

    def inject(
        self,
        name,
        capability
    ):

        self.capabilities[
            name
        ] = capability

    def get(
        self,
        name
    ):

        return self.capabilities.get(name)

    def all_capabilities(self):

        return list(
            self.capabilities.keys()
        )