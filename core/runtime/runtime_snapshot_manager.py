import json
import os
import time
from datetime import datetime, timezone


class RuntimeSnapshotManager:

    def __init__(self, snapshot_dir=None):
        self.snapshot_dir = snapshot_dir or os.path.join(os.getcwd(), "snapshots")
        os.makedirs(self.snapshot_dir, exist_ok=True)
        self._counter = 0

    def _unique_timestamp(self):
        self._counter += 1
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        return f"{ts}_{self._counter:04d}"

    def create_snapshot(self, data, label=None):
        timestamp = self._unique_timestamp()
        name = f"{label}_{timestamp}" if label else timestamp
        path = os.path.join(self.snapshot_dir, f"{name}.json")
        snapshot = {
            "timestamp": timestamp,
            "label": label,
            "runtime_state": data,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, indent=2)
        return path

    def restore_snapshot(self, path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_snapshots(self):
        if not os.path.exists(self.snapshot_dir):
            return []
        return sorted([
            f for f in os.listdir(self.snapshot_dir) if f.endswith(".json")
        ])

    def get_latest(self):
        snapshots = self.list_snapshots()
        if not snapshots:
            return None
        path = os.path.join(self.snapshot_dir, snapshots[-1])
        return self.restore_snapshot(path)

    def delete_snapshot(self, filename):
        path = os.path.join(self.snapshot_dir, filename)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False