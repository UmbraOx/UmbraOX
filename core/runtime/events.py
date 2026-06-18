_event_listeners = {}


def emit(event_type: str, payload: dict):
    """
    Stable event emitter (NO keyword ambiguity)
    """
    if event_type not in _event_listeners:
        return

    for fn in _event_listeners[event_type]:
        fn(payload)


def subscribe(event_type: str, fn):
    if event_type not in _event_listeners:
        _event_listeners[event_type] = []

    _event_listeners[event_type].append(fn)