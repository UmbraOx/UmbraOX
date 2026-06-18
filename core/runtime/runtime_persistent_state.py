import json
from pathlib import Path
import time


class RuntimePersistentState:
    """
    LONG-TERM STATE STORAGE FOR UMBRA

    Stores:
    - last run state
    - last evolution report
    - system health snapshot
    """

    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.state_file = self.base_path / "runtime_state.json"
        self.state_file.parent.mkdir(parents=True, exist_ok=True)

    # -------------------------
    # SAVE STATE
    # -------------------------
    def save(self, data: dict):
        payload = {
            "timestamp": time.time(),
            "data": data
        }

        self.state_file.write_text(
            json.dumps(payload, indent=2),
            encoding="utf-8"
        )

    # -------------------------
    # LOAD STATE
    # -------------------------
    def load(self):
        if not self.state_file.exists():
            return None

        try:
            return json.loads(self.state_file.read_text(encoding="utf-8"))
        except Exception:
            return None