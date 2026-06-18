class RuntimeLiveEventStream:

    def __init__(self):
        self.events = []

    def emit(
        self,
        event
    ):
        self.events.append(event)

    def all(self):
        return self.events