from core.runtime.runtime_safe_executor import (
    RuntimeSafeExecutor
)

from core.runtime.runtime_snapshot_manager import (
    RuntimeSnapshotManager
)

from core.runtime.runtime_backup_system import (
    RuntimeBackupSystem
)


class RuntimeExtensionPipeline:

    def __init__(self):

        self.executor = RuntimeSafeExecutor()

        self.snapshots = RuntimeSnapshotManager()

        self.backups = RuntimeBackupSystem()

    def execute(
        self,
        objective
    ):

        backup = None

        try:

            backup = (
                self.backups.backup_project()
            )

        except Exception as e:

            backup = {
                "success": False,
                "error": str(e)
            }

        result = self.executor.execute(
            objective
        )

        snapshot = (
            self.snapshots.create_snapshot(
                {
                    "objective": objective,
                    "result": result
                }
            )
        )

        return {
            "objective": objective,
            "backup": backup,
            "snapshot": snapshot,
            "execution": result
        }