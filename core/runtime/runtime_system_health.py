from datetime import datetime


class RuntimeSystemHealth:
    """
    Lightweight system health snapshot for Umbra runtime.
    """

    def __init__(self):
        self.boot_time = datetime.now().isoformat()
        self.events = []

    def log_event(self, event_type, message):
        self.events.append(
            {
                "type": event_type,
                "message": message,
                "time": datetime.now().isoformat(),
            }
        )

    def get_health(self):
        return {
            "boot_time": self.boot_time,
            "event_count": len(self.events),
            "recent_events": self.events[-10:],
        }