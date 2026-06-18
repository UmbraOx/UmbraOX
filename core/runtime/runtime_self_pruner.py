import os
from collections import defaultdict


class RuntimeSelfPruner:
    """
    Detects redundant / duplicate / likely-unused runtime modules.
    Generates deletion recommendations (SAFE MODE ONLY).
    """

    def __init__(self, root="core/runtime"):
        self.root = root
        self.last_report = None

    def scan(self):
        files = []

        for r, _, fns in os.walk(self.root):
            for f in fns:
                if f.endswith(".py"):
                    files.append(os.path.join(r, f))

        return files

    def detect_duplicates(self, files):
        name_map = defaultdict(list)

        for f in files:
            name_map[os.path.basename(f)].append(f)

        duplicates = {
            name: paths for name, paths in name_map.items() if len(paths) > 1
        }

        return duplicates

    def generate_report(self):
        files = self.scan()
        duplicates = self.detect_duplicates(files)

        report = {
            "total_files": len(files),
            "duplicate_groups": len(duplicates),
            "duplicates": duplicates,
            "recommendation": "review_duplicates_before_deletion",
        }

        self.last_report = report
        return report

    def get_last_report(self):
        return self.last_report