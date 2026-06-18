class ChangeDetector:

    def detect_changes(self, old_index, new_index):

        old_paths = {
            item["path"]
            for item in old_index
        }

        new_paths = {
            item["path"]
            for item in new_index
        }

        added = list(new_paths - old_paths)
        removed = list(old_paths - new_paths)

        return {
            "added": added,
            "removed": removed
        }