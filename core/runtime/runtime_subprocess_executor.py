import subprocess
import os
import sys
import time
from datetime import datetime


class SubprocessResult:

    def __init__(self, command, returncode, stdout, stderr, duration_seconds):
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
        self.duration_seconds = duration_seconds
        self.success = returncode == 0
        self.executed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "command": self.command,
            "returncode": self.returncode,
            "stdout": self.stdout,
            "stderr": self.stderr,
            "duration_seconds": self.duration_seconds,
            "success": self.success,
            "executed_at": self.executed_at,
        }


class RuntimeSubprocessExecutor:
    """
    Safe subprocess execution with:
    - Configurable timeout
    - Allowlist/blocklist for command safety
    - Working directory isolation
    - Full stdout/stderr capture
    - Execution history
    """

    BLOCKED_COMMANDS = [
        "rm -rf /",
        "format",
        "del /f /s /q c:\\",
        "shutdown",
        "rmdir /s /q c:\\",
    ]

    def __init__(self, working_dir=None, timeout=30, allowed_commands=None):
        self.working_dir = working_dir or os.getcwd()
        self.timeout = timeout
        self.allowed_commands = allowed_commands  # None = allow all non-blocked
        self.execution_history = []

    def execute(self, command, working_dir=None, timeout=None, env_vars=None):
        """
        Execute a shell command safely.
        Returns SubprocessResult.
        """
        work_dir = working_dir or self.working_dir
        time_limit = timeout or self.timeout

        blocked, reason = self._is_blocked(command)
        if blocked:
            result = SubprocessResult(command, -1, "", f"BLOCKED: {reason}", 0)
            self.execution_history.append(result.to_dict())
            return result

        if self.allowed_commands is not None:
            if not self._is_allowed(command):
                result = SubprocessResult(command, -1, "", "BLOCKED: not in allowlist", 0)
                self.execution_history.append(result.to_dict())
                return result

        env = os.environ.copy()
        if env_vars:
            env.update(env_vars)

        start = time.time()
        try:
            proc = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=time_limit,
                cwd=work_dir,
                env=env,
            )
            duration = time.time() - start
            result = SubprocessResult(
                command, proc.returncode, proc.stdout, proc.stderr, round(duration, 3)
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            result = SubprocessResult(command, -1, "", f"TIMEOUT after {time_limit}s", round(duration, 3))
        except Exception as e:
            duration = time.time() - start
            result = SubprocessResult(command, -1, "", f"ERROR: {str(e)}", round(duration, 3))

        self.execution_history.append(result.to_dict())
        return result

    def execute_python(self, script_path, args=None, working_dir=None):
        """Execute a Python script using the current interpreter."""
        python = sys.executable
        arg_str = " ".join(args) if args else ""
        command = f'"{python}" "{script_path}" {arg_str}'.strip()
        return self.execute(command, working_dir=working_dir)

    def execute_pytest(self, test_path="core/tests", working_dir=None):
        """Run pytest on the given path."""
        python = sys.executable
        command = f'"{python}" -m pytest {test_path} -v'
        return self.execute(command, working_dir=working_dir or self.working_dir)

    def execute_pip_install(self, package, working_dir=None):
        """Install a pip package safely."""
        python = sys.executable
        command = f'"{python}" -m pip install {package}'
        return self.execute(command, working_dir=working_dir)

    def _is_blocked(self, command):
        cmd_lower = command.lower().strip()
        for blocked in self.BLOCKED_COMMANDS:
            if blocked.lower() in cmd_lower:
                return True, f"matches blocked pattern: {blocked}"
        return False, ""

    def _is_allowed(self, command):
        if self.allowed_commands is None:
            return True
        cmd_lower = command.lower().strip()
        return any(allowed.lower() in cmd_lower for allowed in self.allowed_commands)

    def get_history(self):
        return list(self.execution_history)

    def get_last_result(self):
        if not self.execution_history:
            return None
        return self.execution_history[-1]

    def clear_history(self):
        self.execution_history.clear()