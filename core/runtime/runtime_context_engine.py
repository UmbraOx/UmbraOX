from core.runtime.runtime_vector_memory import RuntimeVectorMemory


class RuntimeContextEngine:

    def __init__(self):

        self.memory = (
            RuntimeVectorMemory()
        )

    def remember(
        self,
        text,
        metadata=None
    ):

        self.memory.store(
            text,
            metadata
        )

    def recall(
        self,
        query
    ):

        return self.memory.search(
            query
        )