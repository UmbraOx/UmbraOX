from collections import defaultdict


class RuntimeEventBus:

    def __init__(self):

        self.listeners = defaultdict(list)

    def subscribe(
        self,
        event,
        callback
    ):

        self.listeners[event].append(
            callback
        )

    def emit(
        self,
        event,
        payload=None
    ):

        for callback in self.listeners[event]:

            callback(payload)

    def get_registered_events(self):

        return list(
            self.listeners.keys()
        )