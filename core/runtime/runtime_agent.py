from core.runtime.runtime_message import (
    RuntimeMessage
)


class RuntimeAgent:

    def __init__(
        self,
        name,
        message_bus
    ):

        self.name = name

        self.bus = message_bus

    def send_message(
        self,
        recipient,
        message_type,
        payload
    ):

        message = RuntimeMessage(
            sender=self.name,
            recipient=recipient,
            message_type=message_type,
            payload=payload
        )

        self.bus.send(
            message
        )

    def receive_messages(self):

        return self.bus.receive(
            self.name
        )