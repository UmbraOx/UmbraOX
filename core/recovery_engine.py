import os
import shutil


class RecoveryEngine:

    def restore_snapshot(self, snapshot_path, restore_target):

        if not os.path.exists(snapshot_path):
            print("[RECOVERY] Snapshot missing")
            return False

        if os.path.exists(restore_target):
            shutil.rmtree(restore_target)

        shutil.copytree(snapshot_path, restore_target)

        print(f"[RECOVERY] Restored: {restore_target}")

        return True