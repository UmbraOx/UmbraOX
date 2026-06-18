import os
import ast
from collections import defaultdict


class RuntimeDependencyAuditEngine:
    """
    Builds a lightweight dependency map of the runtime system.
    Used for safe deletion recommendations.
    """

    def __init__(self):
        self.import_map = defaultdict(set)
        self.reverse_map = defaultdict(set)

    def scan_directory(self, root_path):
        for root, _, files in os.walk(root_path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    self._scan_file(full_path)

        return self._build_report()

    def _scan_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=file_path)

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        self.import_map[file_path].add(n.name)
                        self.reverse_map[n.name].add(file_path)

                if isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.import_map[file_path].add(node.module)
                        self.reverse_map[node.module].add(file_path)

        except Exception:
            # ignore broken files for now
            pass

    def find_orphans(self):
        orphans = []
        all_files = set(self.import_map.keys())

        for file in all_files:
            if len(self.import_map[file]) == 0:
                orphans.append(file)

        return orphans

    def _build_report(self):
        return {
            "total_files_scanned": len(self.import_map),
            "orphan_candidates": self.find_orphans(),
        }