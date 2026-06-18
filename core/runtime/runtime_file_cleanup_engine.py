import os


class RuntimeFileCleanupEngine:
    """
    Executes safe deletions based on removable file tracker.
    """

    def __init__(self, tracker):
        self.tracker = tracker

    def scan_candidates(self):
        return self.tracker.get_candidates()

    def delete(self, file_path):
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.tracker.unmark(file_path)
                return True
        except Exception:
            pass
        return False

    def cleanup_all(self):
        results = {}

        for file_path in self.scan_candidates():
            results[file_path] = self.delete(file_path)

        return results