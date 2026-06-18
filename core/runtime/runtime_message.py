from datetime import datetime, UTC
from uuid import uuid4


class RuntimeMessage:

    def __init__(
        self,
        sender,
        recipient,
        message_type,
        payload
    ):

        self.id = str(
            uuid4()
        )

        self.sender = sender

        self.recipient = recipient

        self.message_type = (
            message_type
        )

        self.payload = payload

        self.timestamp = (
            datetime.now(UTC)
            .isoformat()
        )

    def to_dict(self):

        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "message_type": (
                self.message_type
            ),
            "payload": self.payload,
            "timestamp": (
                self.timestamp
            )
        }