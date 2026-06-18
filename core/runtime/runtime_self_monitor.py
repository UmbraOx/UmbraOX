class RuntimeSelfMonitor:

    def __init__(self):

        self.events = []

    def monitor(
        self,
        event
    ):

        self.events.append(event)

        return {
            "status": "monitored",
            "event": event
        }