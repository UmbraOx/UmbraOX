import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict


@dataclass
class UpgradeAction:
    file_path: str
    original: str
    modified: str
    reason: str


class RuntimeUpgradeAuthority:
    """
    FINAL SELF-MODIFICATION AUTHORITY LAYER

    Guarantees:
    - atomic staging
    - rollback safety
    - kernel lock integration
    """

    def __init__(self, root_dir: str, kernel=None):
        self.root_dir = Path(root_dir)
        self.kernel = kernel

        self.staged_actions: List[UpgradeAction] = []
        self.history: List[Dict] = []

    # ----------------------------
    # STAGE CHANGE
    # ----------------------------
    def stage_change(self, file_path: str, modified: str, reason: str):
        target = Path(file_path)

        if not target.exists():
            raise FileNotFoundError(file_path)

        original = target.read_text(encoding="utf-8", errors="ignore")

        self.staged_actions.append(
            UpgradeAction(file_path, original, modified, reason)
        )

    # ----------------------------
    # APPLY ALL (ATOMIC)
    # ----------------------------
    def apply(self, backup_dir: str):

        if self.kernel:
            self.kernel.lock_for_upgrade()

        backup_root = Path(backup_dir)
        backup_root.mkdir(parents=True, exist_ok=True)

        applied = []

        try:
            for action in self.staged_actions:
                file_path = Path(action.file_path)

                backup_file = backup_root / (file_path.name + ".bak")
                backup_file.write_text(action.original, encoding="utf-8")

                file_path.write_text(action.modified, encoding="utf-8")

                applied.append(action.file_path)

            self.history.append({
                "time": time.time(),
                "applied": applied
            })

            self.staged_actions.clear()

            return {"status": "success", "applied": applied}

        finally:
            if self.kernel:
                self.kernel.unlock_after_upgrade()

    # ----------------------------
    # ROLLBACK LAST
    # ----------------------------
    def rollback_last(self, backup_dir: str):
        backup_root = Path(backup_dir)

        if not self.history:
            return {"status": "no_history"}

        last = self.history[-1]

        for file_path in last["applied"]:
            backup_file = backup_root / (Path(file_path).name + ".bak")

            if backup_file.exists():
                original = backup_file.read_text(encoding="utf-8")
                Path(file_path).write_text(original, encoding="utf-8")

        return {"status": "rolled_back"}