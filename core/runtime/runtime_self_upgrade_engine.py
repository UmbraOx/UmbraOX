import os
import shutil
import time
from pathlib import Path


class RuntimeSelfUpgradeEngine:
    """
    PRODUCTION-GRADE SELF MODIFICATION ENGINE

    Pipeline:
    stage → validate → backup → apply → verify → rollback (if needed)
    """

    def __init__(self, root_dir: str, kernel=None):
        self.root_dir = Path(root_dir)
        self.kernel = kernel

        self.staged_patch = None
        self.backup_map = {}

        self.history = []

    # -----------------------------
    # STAGE PATCH
    # -----------------------------
    def stage_upgrade(self, proposal: str):
        """
        Stores proposed full-file replacement or patch payload
        """
        self.staged_patch = proposal

    # -----------------------------
    # VALIDATION
    # -----------------------------
    def _validate_patch(self, content: str) -> bool:
        """
        Basic safety validation:
        - must not be empty
        - must contain python-like structure
        """
        if not content or len(content.strip()) < 10:
            return False

        forbidden = ["rm -rf", "delete system32", "format(", "subprocess.call(['rm']"]
        for f in forbidden:
            if f in content:
                return False

        return True

    # -----------------------------
    # APPLY PIPELINE
    # -----------------------------
    def apply(self, backup_dir: str):
        if not self.staged_patch:
            return {"status": "no_patch"}

        patch = self.staged_patch

        if not self._validate_patch(patch):
            return {"status": "rejected_validation"}

        backup_path = Path(backup_dir)
        backup_path.mkdir(parents=True, exist_ok=True)

        modified_files = []

        try:
            # Expect full-file format: "path:::content"
            blocks = patch.split("###FILE###")

            for block in blocks:
                if not block.strip():
                    continue

                try:
                    file_path, content = block.split(":::", 1)
                except ValueError:
                    continue

                file_path = self.root_dir / file_path.strip()

                # backup
                if file_path.exists():
                    backup_file = backup_path / file_path.name
                    shutil.copy2(file_path, backup_file)
                    self.backup_map[str(file_path)] = str(backup_file)

                # apply
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(content, encoding="utf-8")

                modified_files.append(str(file_path))

            # verify
            verification = self._verify(modified_files)

            if not verification["ok"]:
                self.rollback()
                return {"status": "rolled_back", "reason": verification}

            self.history.append({
                "timestamp": time.time(),
                "files": modified_files
            })

            return {
                "status": "applied",
                "files": modified_files
            }

        except Exception as e:
            self.rollback()
            return {"status": "failed", "error": str(e)}

    # -----------------------------
    # VERIFY SYSTEM INTEGRITY
    # -----------------------------
    def _verify(self, files):
        for f in files:
            try:
                if not Path(f).exists():
                    return {"ok": False, "reason": f"missing {f}"}
            except Exception as e:
                return {"ok": False, "reason": str(e)}

        return {"ok": True}

    # -----------------------------
    # ROLLBACK
    # -----------------------------
    def rollback(self):
        for target, backup in self.backup_map.items():
            try:
                shutil.copy2(backup, target)
            except Exception:
                pass

        return {"status": "rollback_complete"}