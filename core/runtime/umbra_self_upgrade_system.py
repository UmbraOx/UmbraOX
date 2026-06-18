from core.runtime.runtime_backup_system import (
    RuntimeBackupSystem
)

from core.runtime.runtime_snapshot_manager import (
    RuntimeSnapshotManager
)


class UmbraSelfUpgradeSystem:

    def __init__(self):
        self.backups = (
            RuntimeBackupSystem()
        )

        self.snapshots = (
            RuntimeSnapshotManager()
        )

    def safeguard(self):
        backup = (
            self.backups.backup_project()
        )

        snapshot = (
            self.snapshots.create_snapshot({
                "runtime": "upgrade_ready"
            })
        )

        return {
            "backup": backup,
            "snapshot": snapshot
        }