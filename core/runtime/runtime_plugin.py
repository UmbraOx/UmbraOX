class RuntimePlugin:

    def __init__(
        self,
        name,
        version="1.0"
    ):

        self.name = name
        self.version = version

    def initialize(self):

        return {
            "success": True,
            "plugin": self.name
        }