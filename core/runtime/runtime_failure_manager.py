from core.runtime.runtime_repair_engine import (
    RuntimeRepairEngine
)


class RuntimeFailureManager:

    def __init__(self):

        self.repair = (
            RuntimeRepairEngine()
        )

        self.failures = []

    def record(self, error):

        payload = {
            "error": str(error)
        }

        self.failures.append(
            payload
        )

        repaired = (
            self.repair.repair(error)
        )

        return {
            "failure": payload,
            "repair": repaired
        }

    def all(self):

        return self.failures