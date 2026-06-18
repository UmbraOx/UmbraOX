import subprocess
import sys
import os
import tempfile
from datetime import datetime


class RunResult:

    def __init__(self, success, stdout, stderr, returncode, duration, file_path=""):
        self.success = success
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode
        self.duration = duration
        self.file_path = file_path
        self.ran_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "success": self.success,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "returncode": self.returncode,
            "duration": self.duration,
            "file_path": self.file_path,
            "ran_at": self.ran_at,
        }


class RuntimeCodeRunner:
    """
    Execute generated Python code safely.
    - Run .py files from workspace
    - Run code strings via temp files
    - Capture stdout/stderr
    - Timeout protection
    - Execution history
    """

    def __init__(self, timeout=15, working_dir=None):
        self.timeout = timeout
        self.working_dir = working_dir or os.getcwd()
        self.run_history = []

    def run_file(self, file_path, args=None, timeout=None):
        import time
        if not os.path.exists(file_path):
            result = RunResult(False, "", f"File not found: {file_path}", -1, 0, file_path)
            self.run_history.append(result.to_dict())
            return result

        cmd = [sys.executable, file_path]
        if args:
            cmd.extend(args)

        start = time.time()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout or self.timeout,
                cwd=self.working_dir,
            )
            duration = round(time.time() - start, 3)
            result = RunResult(
                proc.returncode == 0,
                proc.stdout,
                proc.stderr,
                proc.returncode,
                duration,
                file_path,
            )
        except subprocess.TimeoutExpired:
            duration = round(time.time() - start, 3)
            result = RunResult(False, "", f"TIMEOUT after {timeout or self.timeout}s", -1, duration, file_path)
        except Exception as e:
            duration = round(time.time() - start, 3)
            result = RunResult(False, "", str(e), -1, duration, file_path)

        self.run_history.append(result.to_dict())
        return result

    def run_string(self, code, timeout=None):
        import time
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(code)
            tmp_path = f.name
        try:
            return self.run_file(tmp_path, timeout=timeout)
        finally:
            try:
                os.unlink(tmp_path)
            except Exception:
                pass

    def run_workspace_file(self, workspace_path, relative_code_path, timeout=None):
        full_path = os.path.join(workspace_path, relative_code_path)
        return self.run_file(full_path, timeout=timeout)

    def get_history(self):
        return list(self.run_history)

    def get_last_result(self):
        return self.run_history[-1] if self.run_history else None

    def clear_history(self):
        self.run_history.clear()