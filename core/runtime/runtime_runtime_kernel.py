class RuntimeKernel:

    def __init__(self):

        self.initialized = False

    def boot(self):

        self.initialized = True

        return {
            "status": "booted"
        }