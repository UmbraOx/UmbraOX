import os
import subprocess
import sys
from datetime import datetime


class AutoTestResult:

    def __init__(self, passed, failed, errors, skipped, duration, output):
        self.passed = passed
        self.failed = failed
        self.errors = errors
        self.skipped = skipped
        self.duration = duration
        self.output = output
        self.success = failed == 0 and errors == 0
        self.ran_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "passed": self.passed,
            "failed": self.failed,
            "errors": self.errors,
            "skipped": self.skipped,
            "duration": self.duration,
            "success": self.success,
            "ran_at": self.ran_at,
        }

    def summary(self):
        return (
            f"{'PASS' if self.success else 'FAIL'} "
            f"passed={self.passed} failed={self.failed} "
            f"errors={self.errors} skipped={self.skipped} "
            f"({self.duration:.1f}s)"
        )


class RuntimeAutoTester:
    """
    Autonomous test runner.
    - Runs pytest on specified paths
    - Parses results into structured data
    - Tracks test history
    - Can run tests on generated code
    """

    def __init__(self, project_root=None, timeout=60):
        self.project_root = project_root or os.getcwd()
        self.timeout = timeout
        self.test_history = []

    def run_tests(self, test_path="core/tests", extra_args=None):
        cmd = [sys.executable, "-m", "pytest", test_path, "-v", "--timeout=30", "--tb=short"]
        if extra_args:
            cmd.extend(extra_args)

        import time
        start = time.time()
        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                cwd=self.project_root,
            )
            duration = time.time() - start
            output = proc.stdout + proc.stderr
            result = self._parse_result(output, duration)
        except subprocess.TimeoutExpired:
            duration = time.time() - start
            result = AutoTestResult(0, 0, 1, 0, duration, "TIMEOUT")
        except Exception as e:
            duration = time.time() - start
            result = AutoTestResult(0, 0, 1, 0, duration, str(e))

        self.test_history.append(result.to_dict())
        return result

    def run_single_file(self, test_file_path):
        return self.run_tests(test_path=test_file_path)

    def run_generated_code_tests(self, workspace_path):
        test_files = []
        for root, _, files in os.walk(workspace_path):
            for f in files:
                if f.startswith("test_") and f.endswith(".py"):
                    test_files.append(os.path.join(root, f))
        if not test_files:
            return None
        return self.run_tests(test_path=" ".join(test_files))

    def _parse_result(self, output, duration):
        import re
        passed = failed = errors = skipped = 0
        for line in output.splitlines():
            if " passed" in line or " failed" in line or " error" in line:
                p = re.search(r"(\d+) passed", line)
                f = re.search(r"(\d+) failed", line)
                e = re.search(r"(\d+) error", line)
                s = re.search(r"(\d+) skipped", line)
                if p:
                    passed = int(p.group(1))
                if f:
                    failed = int(f.group(1))
                if e:
                    errors = int(e.group(1))
                if s:
                    skipped = int(s.group(1))
        return AutoTestResult(passed, failed, errors, skipped, duration, output[-3000:])

    def get_history(self):
        return list(self.test_history)

    def get_last_result(self):
        return self.test_history[-1] if self.test_history else None

    def is_suite_passing(self):
        if not self.test_history:
            return None
        last = self.test_history[-1]
        return last["success"]