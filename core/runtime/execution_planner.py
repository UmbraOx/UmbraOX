from core.runtime.task_graph import (
    TaskGraph
)

from core.runtime.agent_task_distributor import (
    AgentTaskDistributor
)


class ExecutionPlanner:

    def __init__(self):

        self.graph_builder = (
            TaskGraph()
        )

        self.distributor = (
            AgentTaskDistributor()
        )

    def plan(self, proposal):

        graph = (
            self.graph_builder.build(
                proposal
            )
        )

        assignments = (
            self.distributor.distribute(
                graph
            )
        )

        return {
            "graph": graph,
            "assignments": assignments
        }