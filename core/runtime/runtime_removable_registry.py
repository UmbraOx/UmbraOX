from datetime import datetime


class RuntimeRemovableRegistry:
    def __init__(self):
        self.registry = {}

    def mark(self, path, reason="generated"):
        self.registry[path] = {
            "reason": reason,
            "marked_at": datetime.now().isoformat()
        }

    def unmark(self, path):
        self.registry.pop(path, None)

    def list_removable(self):
        return list(self.registry.keys())

    def is_removable(self, path):
        return path in self.registry

    def export_report(self):
        return self.registry