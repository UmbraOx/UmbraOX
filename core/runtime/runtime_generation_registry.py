class RuntimeGenerationRegistry:

    def __init__(self):
        self.generated = []

    def track(self, path):
        self.generated.append(path)

    def all(self):
        return self.generated