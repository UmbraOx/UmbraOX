class RuntimeCodeRegistry:

    def __init__(self):
        self.code = []

    def add(self, module):
        self.code.append(module)

    def all(self):
        return self.code