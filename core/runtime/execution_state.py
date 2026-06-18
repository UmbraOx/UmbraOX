# core/runtime/execution_state.py

from core.runtime.events import emit


class ExecutionState:
    def started(self, tool, task_id=None):
        emit("state_started", {"tool": tool, "task_id": task_id})

    def completed(self, tool, task_id=None):
        emit("state_completed", {"tool": tool, "task_id": task_id})

    def failed(self, tool, error=None, task_id=None):
        emit("state_failed", {
            "tool": tool,
            "error": str(error),
            "task_id": task_id
        })