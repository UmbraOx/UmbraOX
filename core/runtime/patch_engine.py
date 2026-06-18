# core/runtime/patch_engine.py

import os
import shutil
from datetime import datetime


class PatchEngine:

    def __init__(self):

        self.snapshot_dir = "runtime_snapshots"

        os.makedirs(self.snapshot_dir, exist_ok=True)

    # -------------------------------------------------
    # SNAPSHOT
    # -------------------------------------------------

    def create_snapshot(self, filepath):

        if not os.path.exists(filepath):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        filename = os.path.basename(filepath)

        snapshot_name = f"{timestamp}_{filename}"

        snapshot_path = os.path.join(
            self.snapshot_dir,
            snapshot_name
        )

        shutil.copy2(filepath, snapshot_path)

        print(f"[PATCH] snapshot created: {snapshot_name}")

        return snapshot_path

    # -------------------------------------------------
    # APPLY PATCH
    # -------------------------------------------------

    def apply_patch(self, filepath, new_content):

        # snapshot first
        self.create_snapshot(filepath)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"[PATCH] updated: {filepath}")

        return {
            "status": "patched",
            "file": filepath
        }

    # -------------------------------------------------
    # RESTORE
    # -------------------------------------------------

    def restore_snapshot(self, snapshot_path, target_path):

        shutil.copy2(snapshot_path, target_path)

        print(f"[PATCH] restored: {target_path}")

        return {
            "status": "restored",
            "target": target_path
        }