from core.runtime.umbra_self_repair_core import CodebaseObserver, DependencyGraph
from pathlib import Path


class ScannerAgent:

    def __init__(self, root: str):
        self.root = Path(root)
        self.observer = CodebaseObserver()
        self.graph = DependencyGraph()

    def scan(self):

        nodes = []

        for file in self.root.rglob("*.py"):
            node = self.observer.scan_file(file)
            if node:
                nodes.append(node)
                self.graph.add(node)

        return {
            "nodes": nodes,
            "graph": self.graph
        }