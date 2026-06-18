class RuntimeCommandProcessor:
    def __init__(self):
        self.history = []

    def process(self, command: str):
        normalized = command.strip()

        result = {
            "command": normalized,
            "status": "accepted",
        }

        self.history.append(result)

        return result

    def get_history(self):
        return self.history