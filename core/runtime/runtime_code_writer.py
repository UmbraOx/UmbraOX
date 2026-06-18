import os
import ast
from datetime import datetime


class WriteResult:

    def __init__(self, success, path, message="", backup_path=None):
        self.success = success
        self.path = path
        self.message = message
        self.backup_path = backup_path
        self.written_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "success": self.success,
            "path": self.path,
            "message": self.message,
            "backup_path": self.backup_path,
            "written_at": self.written_at,
        }


class RuntimeCodeWriter:
    """
    Writes real Python files to disk autonomously.
    - Validates syntax before writing
    - Creates backups of existing files before overwriting
    - Tracks all writes this session
    - Supports atomic write (write to temp then rename)
    - Can write to workspace or direct project paths
    """

    def __init__(self, base_dir=None, backup_dir=None, validate_before_write=True):
        self.base_dir = base_dir or os.getcwd()
        self.backup_dir = backup_dir or os.path.join(self.base_dir, ".umbra_backups")
        self.validate_before_write = validate_before_write
        self.write_history = []

    def write(self, relative_path, content, overwrite=True):
        """
        Write content to a file relative to base_dir.
        Validates Python syntax first, backs up existing file.
        Returns WriteResult.
        """
        full_path = os.path.join(self.base_dir, relative_path)

        # Syntax validation for .py files
        if relative_path.endswith(".py") and self.validate_before_write:
            valid, error = self._validate_syntax(content)
            if not valid:
                result = WriteResult(False, full_path, f"Syntax error: {error}")
                self.write_history.append(result.to_dict())
                return result

        # Backup existing file
        backup_path = None
        if os.path.exists(full_path):
            if not overwrite:
                result = WriteResult(False, full_path, "File exists and overwrite=False")
                self.write_history.append(result.to_dict())
                return result
            backup_path = self._backup(full_path)

        # Ensure directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True) if os.path.dirname(full_path) else None

        # Atomic write via temp file
        tmp_path = full_path + ".umbra_tmp"
        try:
            with open(tmp_path, "w", encoding="utf-8") as f:
                f.write(content)
            os.replace(tmp_path, full_path)
            result = WriteResult(True, full_path, "Written successfully", backup_path)
        except Exception as e:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
            result = WriteResult(False, full_path, f"Write error: {str(e)}", backup_path)

        self.write_history.append(result.to_dict())
        return result

    def write_absolute(self, absolute_path, content, overwrite=True):
        """Write to an absolute path."""
        rel = os.path.relpath(absolute_path, self.base_dir)
        return self.write(rel, content, overwrite=overwrite)

    def write_many(self, file_dict, overwrite=True):
        """
        Write multiple files at once.
        file_dict: {relative_path: content}
        Returns list of WriteResults.
        """
        results = []
        for path, content in file_dict.items():
            results.append(self.write(path, content, overwrite=overwrite))
        return results

    def read(self, relative_path):
        """Read a file relative to base_dir."""
        full_path = os.path.join(self.base_dir, relative_path)
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()

    def exists(self, relative_path):
        return os.path.exists(os.path.join(self.base_dir, relative_path))

    def delete(self, relative_path, backup_first=True):
        full_path = os.path.join(self.base_dir, relative_path)
        if not os.path.exists(full_path):
            return False
        if backup_first:
            self._backup(full_path)
        os.remove(full_path)
        return True

    def list_python_files(self, subdir=""):
        """List all .py files under base_dir/subdir."""
        search_root = os.path.join(self.base_dir, subdir) if subdir else self.base_dir
        py_files = []
        for root, dirs, files in os.walk(search_root):
            # Skip venv and hidden dirs
            dirs[:] = [d for d in dirs if d not in ("venv", ".git", "__pycache__", ".umbra_backups")]
            for fname in files:
                if fname.endswith(".py"):
                    full = os.path.join(root, fname)
                    py_files.append(os.path.relpath(full, self.base_dir))
        return py_files

    def restore_backup(self, relative_path):
        """Restore the most recent backup of a file."""
        full_path = os.path.join(self.base_dir, relative_path)
        fname = os.path.basename(full_path)
        os.makedirs(self.backup_dir, exist_ok=True)
        backups = sorted([
            f for f in os.listdir(self.backup_dir)
            if f.startswith(fname + ".bak_")
        ], reverse=True)
        if not backups:
            return False
        latest = os.path.join(self.backup_dir, backups[0])
        import shutil
        shutil.copy2(latest, full_path)
        return True

    def get_write_history(self):
        return list(self.write_history)

    def get_failed_writes(self):
        return [r for r in self.write_history if not r["success"]]

    def _validate_syntax(self, content):
        try:
            ast.parse(content)
            return True, None
        except SyntaxError as e:
            return False, f"line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)

    def _backup(self, full_path):
        os.makedirs(self.backup_dir, exist_ok=True)
        fname = os.path.basename(full_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        backup_path = os.path.join(self.backup_dir, f"{fname}.bak_{timestamp}")
        import shutil
        shutil.copy2(full_path, backup_path)
        return backup_path