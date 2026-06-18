class RuntimePluginInterface:

    def initialize(self):
        raise NotImplementedError

    def execute(
        self,
        payload
    ):
        raise NotImplementedError