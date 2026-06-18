class RuntimeMemoryIndex:

    def __init__(self):

        self.index = {}

    def store(
        self,
        key,
        value
    ):

        self.index[key] = value

    def retrieve(
        self,
        key
    ):

        return self.index.get(key)

    def keys(self):

        return list(
            self.index.keys()
        )