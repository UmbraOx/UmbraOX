import uuid
from datetime import datetime


class ExecutionNode:
    STATE_PENDING = "pending"
    STATE_READY = "ready"
    STATE_RUNNING = "running"
    STATE_COMPLETED = "completed"
    STATE_FAILED = "failed"
    STATE_SKIPPED = "skipped"

    def __init__(self, task_id, task_data=None):
        self.node_id = str(uuid.uuid4())
        self.task_id = task_id
        self.task_data = task_data or {}

        self.state = self.STATE_PENDING
        self.dependencies = []
        self.dependents = []

        self.result = None
        self.error = None

        self.retry_count = 0
        self.max_retries = 3

        self.created_at = datetime.now().isoformat()
        self.started_at = None
        self.completed_at = None

    def mark_running(self):
        self.state = self.STATE_RUNNING
        self.started_at = datetime.now().isoformat()

    def mark_completed(self, result=None):
        self.state = self.STATE_COMPLETED
        self.result = result
        self.completed_at = datetime.now().isoformat()

    def mark_failed(self, error=None):
        self.state = self.STATE_FAILED
        self.error = error
        self.completed_at = datetime.now().isoformat()

    def mark_skipped(self):
        self.state = self.STATE_SKIPPED
        self.completed_at = datetime.now().isoformat()

    def is_terminal(self):
        return self.state in {
            self.STATE_COMPLETED,
            self.STATE_FAILED,
            self.STATE_SKIPPED,
        }

    def to_dict(self):
        return self.__dict__


class RuntimeExecutionGraph:
    """
    DAG execution graph for task orchestration.
    """

    def __init__(self):
        self.nodes = {}
        self.task_index = {}
        self.execution_log = []

    def add_node(self, task_id, task_data=None):
        if task_id in self.task_index:
            return self.nodes[self.task_index[task_id]]

        node = ExecutionNode(task_id, task_data)
        self.nodes[node.node_id] = node
        self.task_index[task_id] = node.node_id

        self._log(f"added:{task_id}")
        return node

    def add_edge(self, from_task_id, to_task_id):
        from_node = self.add_node(from_task_id)
        to_node = self.add_node(to_task_id)

        from_node.dependents.append(to_node.node_id)
        to_node.dependencies.append(from_node.node_id)

        self._log(f"edge:{from_task_id}->{to_task_id}")

    def mark_node_running(self, task_id):
        node = self.get_by_task(task_id)
        if node:
            node.mark_running()

    def mark_node_completed(self, task_id, result=None):
        node = self.get_by_task(task_id)
        if node:
            node.mark_completed(result)

    def mark_node_failed(self, task_id, error=None, propagate=False):
        node = self.get_by_task(task_id)
        if node:
            node.mark_failed(error)

    def get_by_task(self, task_id):
        node_id = self.task_index.get(task_id)
        if not node_id:
            return None
        return self.nodes.get(node_id)

    def summary(self):
        return {
            "total_nodes": len(self.nodes),
            "tasks_indexed": len(self.task_index),
            "log_size": len(self.execution_log),
        }

    def _log(self, event):
        self.execution_log.append(
            {
                "event": event,
                "time": datetime.now().isoformat(),
            }
        )