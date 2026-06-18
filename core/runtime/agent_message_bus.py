class AgentMessageBus:

    def __init__(self):

        self.messages = []

    def send(
        self,
        sender,
        target,
        payload
    ):

        message = {
            "sender": sender,
            "target": target,
            "payload": payload
        }

        self.messages.append(message)

    def fetch(
        self,
        target
    ):

        results = []

        remaining = []

        for message in self.messages:

            if message["target"] == target:
                results.append(message)

            else:
                remaining.append(message)

        self.messages = remaining

        return results