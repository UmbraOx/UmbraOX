import os
import difflib
import shutil
from datetime import datetime


class PatchResult:
    def __init__(self, path, success, diff, backup_path=None, error=None):
        self.path = path
        self.success = success
        self.diff = diff
        self.backup_path = backup_path
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def to_dict(self):
        return self.__dict__


class RuntimePatchEngine:
    """
    Safe self-modification engine:
    - generates diffs
    - creates backups
    - applies patches
    - supports rollback
    """

    def __init__(self, backup_dir=None):
        self.backup_dir = backup_dir or os.path.join(
            os.getcwd(), "sessions", "patch_backups"
        )
        os.makedirs(self.backup_dir, exist_ok=True)

        self.history = []

    def generate_diff(self, original_content, new_content, path):
        diff = difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"a/{path}",
            tofile=f"b/{path}",
        )
        return "".join(diff)

    def apply_patch(self, file_path, new_content, auto_backup=True):
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                original = f.read()

            diff = self.generate_diff(original, new_content, file_path)

            backup_path = None
            if auto_backup:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_path = os.path.join(
                    self.backup_dir,
                    f"{os.path.basename(file_path)}.{ts}.bak",
                )
                shutil.copy2(file_path, backup_path)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)

            result = PatchResult(
                path=file_path,
                success=True,
                diff=diff,
                backup_path=backup_path,
            )

        except Exception as e:
            result = PatchResult(
                path=file_path,
                success=False,
                diff="",
                error=str(e),
            )

        self.history.append(result.to_dict())
        return result

    def rollback(self, backup_path, target_path):
        try:
            shutil.copy2(backup_path, target_path)
            return {"success": True, "rolled_back": target_path}
        except Exception as e:
            return {"success": False, "error": str(e)}