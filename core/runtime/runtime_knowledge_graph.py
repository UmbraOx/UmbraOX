from __future__ import annotations


class RuntimeKnowledgeGraph:
    def __init__(self):
        self.nodes = set()
        self.edges = []

    def add_node(self, node: str):
        self.nodes.add(node)

    def add_edge(self, source: str, target: str):
        self.edges.append({
            "source": source,
            "target": target,
        })