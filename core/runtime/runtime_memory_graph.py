class RuntimeMemoryGraph:

    def __init__(self):
        self.nodes = []

    def add(
        self,
        node
    ):
        self.nodes.append(node)

    def all(self):
        return self.nodes