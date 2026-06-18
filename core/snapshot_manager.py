import os
import json
import shutil
from datetime import datetime


class SnapshotManager:

    def __init__(self):
        self.snapshot_root = "memory/snapshots"

        os.makedirs(self.snapshot_root, exist_ok=True)

    def create_snapshot(self, target_path):

        if not os.path.exists(target_path):
            print(f"[SNAPSHOT] Missing target: {target_path}")
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        snapshot_name = f"snapshot_{timestamp}"

        snapshot_path = os.path.join(
            self.snapshot_root,
            snapshot_name
        )

        shutil.copytree(target_path, snapshot_path)

        metadata = {
            "timestamp": timestamp,
            "source": target_path,
            "snapshot": snapshot_path
        }

        metadata_file = os.path.join(
            snapshot_path,
            "snapshot.json"
        )

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"[SNAPSHOT] Created: {snapshot_path}")

        return snapshot_path