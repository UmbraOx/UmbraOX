from datetime import UTC
from datetime import datetime


class RuntimeExecutionHistory:

    def __init__(self):

        self.history = []

    def record(
        self,
        task,
        success,
        metadata=None
    ):

        self.history.append(
            {
                "task": task,
                "success": success,
                "metadata": metadata or {},
                "timestamp": (
                    datetime.now(UTC).isoformat()
                )
            }
        )

    def get_history(self):

        return self.history