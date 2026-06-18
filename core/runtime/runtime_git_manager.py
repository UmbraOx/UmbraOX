import os
import subprocess
import sys
from datetime import datetime


class GitResult:

    def __init__(self, success, command, output, error=""):
        self.success = success
        self.command = command
        self.output = output
        self.error = error
        self.executed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "success": self.success,
            "command": self.command,
            "output": self.output,
            "error": self.error,
            "executed_at": self.executed_at,
        }


class RuntimeGitManager:
    """
    Git operations for autonomous project management.
    - init, status, add, commit, diff, log, branch
    - Safe execution with output capture
    - Works on any directory
    """

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        self.operation_history = []

    def _run(self, args):
        try:
            result = subprocess.run(
                ["git"] + args,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
                timeout=30,
            )
            success = result.returncode == 0
            output = result.stdout.strip()
            error = result.stderr.strip()
            git_result = GitResult(success, "git " + " ".join(args), output, error)
        except FileNotFoundError:
            git_result = GitResult(False, "git " + " ".join(args), "", "git not found in PATH")
        except subprocess.TimeoutExpired:
            git_result = GitResult(False, "git " + " ".join(args), "", "timeout")
        except Exception as e:
            git_result = GitResult(False, "git " + " ".join(args), "", str(e))

        self.operation_history.append(git_result.to_dict())
        return git_result

    def init(self):
        return self._run(["init"])

    def status(self):
        return self._run(["status", "--short"])

    def add(self, path="."):
        return self._run(["add", path])

    def commit(self, message):
        return self._run(["commit", "-m", message])

    def add_and_commit(self, message, path="."):
        self.add(path)
        return self.commit(message)

    def diff(self, staged=False):
        args = ["diff"]
        if staged:
            args.append("--staged")
        return self._run(args)

    def log(self, count=10):
        return self._run(["log", f"--oneline", f"-{count}"])

    def branch(self):
        return self._run(["branch"])

    def current_branch(self):
        result = self._run(["rev-parse", "--abbrev-ref", "HEAD"])
        return result.output if result.success else "unknown"

    def is_repo(self):
        result = self._run(["rev-parse", "--is-inside-work-tree"])
        return result.success and result.output == "true"

    def has_uncommitted_changes(self):
        result = self.status()
        return result.success and len(result.output) > 0

    def create_branch(self, branch_name):
        return self._run(["checkout", "-b", branch_name])

    def checkout(self, branch_name):
        return self._run(["checkout", branch_name])

    def get_history(self):
        return list(self.operation_history)

    def set_repo_path(self, path):
        self.repo_path = path