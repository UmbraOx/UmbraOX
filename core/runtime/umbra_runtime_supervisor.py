from core.runtime.runtime_runtime_repair_engine import (
    RuntimeRepairEngine
)


class UmbraRuntimeSupervisor:

    def __init__(self):
        self.repair = (
            RuntimeRepairEngine()
        )

    def recover(
        self,
        error
    ):
        return self.repair.repair(
            error
        )