class FailureMemory:

    def __init__(self):

        self.failures = []

    def record(
        self,
        source,
        error
    ):

        entry = {
            "source": source,
            "error": error
        }

        self.failures.append(entry)

        print(
            f"[FAILURE_MEMORY] recorded: {source}"
        )

    def get_failures(self):

        return self.failures