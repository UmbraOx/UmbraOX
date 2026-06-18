import time


class ExecutionSnapshotEngine:

    def snapshot(
        self,
        state
    ):

        return {
            "timestamp": time.time(),
            "state": state
        }