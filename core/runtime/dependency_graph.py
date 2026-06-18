import ast
import os
from collections import defaultdict


class DependencyGraph:
    """
    Builds a lightweight import + dependency graph of the Umbra system.
    """

    def __init__(self, root="core"):
        self.root = root
        self.graph = defaultdict(set)

    def build(self):
        for dirpath, _, filenames in os.walk(self.root):
            for file in filenames:
                if not file.endswith(".py"):
                    continue

                path = os.path.join(dirpath, file)
                self._parse_file(path)

        return dict(self.graph)

    def _parse_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                tree = ast.parse(f.read(), filename=path)

            module = path.replace("\\", "/")

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for n in node.names:
                        self.graph[module].add(n.name)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        self.graph[module].add(node.module)

        except Exception:
            # fail silently to avoid breaking scan
            pass

    def get_graph(self):
        return dict(self.graph)