from datetime import datetime
from datetime import UTC

import traceback


class RuntimeSafeExecutor:

    def __init__(self):

        self.execution_history = []

    def execute(
        self,
        objective
    ):

        started = (
            datetime.now(UTC)
            .isoformat()
        )

        result = {
            "success": True,
            "objective": objective,
            "started": started,
            "completed": None,
            "error": None,
            "traceback": None
        }

        try:

            simulated_result = {
                "status": "executed",
                "objective": objective
            }

            result["result"] = (
                simulated_result
            )

        except Exception as e:

            result["success"] = False

            result["error"] = str(e)

            result["traceback"] = (
                traceback.format_exc()
            )

        result["completed"] = (
            datetime.now(UTC)
            .isoformat()
        )

        self.execution_history.append(
            result
        )

        return result

    def get_history(self):

        return self.execution_history