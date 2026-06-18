from datetime import datetime
from datetime import UTC


class RuntimeProjectGraph:

    def __init__(self):

        self.nodes = []

        self.edges = []

        self.history = []

    def add_node(
        self,
        node
    ):

        if node not in self.nodes:

            self.nodes.append(node)

    def add_edge(
        self,
        source,
        target
    ):

        edge = {
            "source": source,
            "target": target
        }

        if edge not in self.edges:

            self.edges.append(edge)

    def record_event(
        self,
        event
    ):

        history_event = {
            "event": event,
            "time": (
                datetime.now(UTC)
                .isoformat()
            )
        }

        self.history.append(
            history_event
        )

        goal = event.get("goal")

        dependencies = event.get(
            "dependencies",
            []
        )

        if goal:

            self.add_node(goal)

        for dependency in dependencies:

            self.add_node(
                dependency
            )

            self.add_edge(
                dependency,
                goal
            )

    def get_graph(self):

        return {
            "nodes": self.nodes,
            "edges": self.edges
        }

    def get_history(self):

        return self.history

    def clear(self):

        self.nodes = []

        self.edges = []

        self.history = []