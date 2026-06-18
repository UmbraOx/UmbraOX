class RuntimeEventStream:

    def __init__(self):

        self.events = []

    def emit(
        self,
        event,
        payload=None
    ):

        self.events.append({
            "event": event,
            "payload": payload
        })

    def history(self):

        return self.events