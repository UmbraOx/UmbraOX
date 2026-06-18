from collections import defaultdict


class RuntimeMessageBus:

    def __init__(self):

        self.messages = defaultdict(
            list
        )

    def send(
        self,
        message
    ):

        self.messages[
            message.recipient
        ].append(
            message.to_dict()
        )

    def receive(
        self,
        recipient
    ):

        queue = self.messages[
            recipient
        ]

        self.messages[
            recipient
        ] = []

        return queue

    def pending_count(
        self,
        recipient
    ):

        return len(
            self.messages[
                recipient
            ]
        )