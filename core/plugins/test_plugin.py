class Plugin:

    def __init__(self):

        self.name = "test_plugin"
        self.description = ""

    def run(self, *args, **kwargs):

        print("[PLUGIN] Running plugin: test_plugin")
