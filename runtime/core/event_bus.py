# core/runtime/event_bus.py

from collections import defaultdict
import threading

class EventBus:
    def __init__(self):
        self.listeners = defaultdict(list)
        self.lock = threading.Lock()

    def subscribe(self, event_type, callback):
        with self.lock:
            self.listeners[event_type].append(callback)

    def emit(self, event_type, data=None):
        with self.lock:
            callbacks = list(self.listeners.get(event_type, []))

        for cb in callbacks:
            try:
                cb(data)
            except Exception as e:
                print(f"[EventBus Error] {event_type}: {e}")