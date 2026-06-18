class UmbraAgentCommunicationBus:

    def __init__(self):
        self.messages = []

    def send(
        self,
        sender,
        target,
        message
    ):
        payload = {
            "sender": sender,
            "target": target,
            "message": message
        }

        self.messages.append(
            payload
        )

        return payload

    def all(self):
        return self.messages