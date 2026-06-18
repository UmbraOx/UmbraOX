import time


def format_event(event_type, data):
    return {
        "event": event_type,
        "timestamp": int(time.time()),
        "data": data or {}
    }