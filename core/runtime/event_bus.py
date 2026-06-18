from collections import defaultdict


class EventBus:
    """
    Simple in-memory pub/sub system for UI + runtime sync
    """

    def __init__(self):
        self.subscribers = defaultdict(list)

    def emit(self, event_type: str, payload=None):
        if payload is None:
            payload = {}

        if event_type not in self.subscribers:
            return

        for callback in self.subscribers[event_type]:
            try:
                callback(payload)
            except Exception:
                pass

    def subscribe(self, event_type: str, callback):
        self.subscribers[event_type].append(callback)


# global singleton
event_bus = EventBus()


# convenience wrappers (IMPORTANT: fixes your earlier errors)
def emit(event_type: str, payload=None):
    return event_bus.emit(event_type, payload)


def subscribe(event_type: str, callback):
    return event_bus.subscribe(event_type, callback)