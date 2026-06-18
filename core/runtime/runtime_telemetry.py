from datetime import UTC
from datetime import datetime


class RuntimeTelemetry:

    def __init__(self):

        self.events = []

    def record(
        self,
        event,
        metadata=None
    ):

        self.events.append(
            {
                "event": event,
                "metadata": metadata or {},
                "timestamp": (
                    datetime.now(UTC).isoformat()
                )
            }
        )

    def get_events(self):

        return self.events