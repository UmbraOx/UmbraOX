import os
import json
from datetime import datetime


class RuntimeRemovableFileTracker:
    """
    Tracks files that Umbra considers:
    - generated
    - temporary
    - redundant
    - safe-to-delete candidates
    """

    def __init__(self, path=None):
        self.path = path or os.path.join(
            os.getcwd(), "sessions", "removable_files.json"
        )
        self.files = {}

        self._load()

    def mark(self, file_path, reason="unknown"):
        self.files[file_path] = {
            "reason": reason,
            "marked_at": datetime.now().isoformat(),
        }
        return True

    def unmark(self, file_path):
        return self.files.pop(file_path, None) is not None

    def list(self):
        return self.files

    def get_candidates(self):
        return list(self.files.keys())

    def save(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.files, f, indent=2)

    def _load(self):
        if not os.path.exists(self.path):
            return
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self.files = json.load(f)
        except Exception:
            self.files = {}