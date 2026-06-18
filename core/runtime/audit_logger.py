import json
import time
import os

class AuditLogger:

    def __init__(self, path="audit_log.json"):
        self.path = path
        self.logs = []

    def log(self, event_type: str, data=None):
        entry = {
            "time": time.time(),
            "event": event_type,
            "data": data
        }

        self.logs.append(entry)
        self._persist()

    def _persist(self):
        with open(self.path, "w") as f:
            json.dump(self.logs, f, indent=2)


audit_logger = AuditLogger()