import os
import sys
from datetime import datetime


class HealthReport:

    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.checks = []
        self.overall_status = "healthy"

    def add_check(self, name, status, message="", severity="info"):
        self.checks.append({
            "name": name,
            "status": status,
            "message": message,
            "severity": severity,
        })
        if status == "fail" and severity == "critical":
            self.overall_status = "critical"
        elif status == "warn" and self.overall_status == "healthy":
            self.overall_status = "degraded"

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "overall_status": self.overall_status,
            "checks": self.checks,
            "pass_count": sum(1 for c in self.checks if c["status"] == "pass"),
            "warn_count": sum(1 for c in self.checks if c["status"] == "warn"),
            "fail_count": sum(1 for c in self.checks if c["status"] == "fail"),
        }

    def summary_line(self):
        d = self.to_dict()
        return (
            f"[{self.overall_status.upper()}] "
            f"pass={d['pass_count']} warn={d['warn_count']} fail={d['fail_count']}"
        )


class RuntimeHealthMonitor:
    """
    Runtime health and integrity checks.
    - Checks Ollama connectivity
    - Validates directory structure
    - Checks Python environment
    - Monitors disk space
    - Verifies key runtime files exist
    """

    REQUIRED_DIRS = ["core/runtime", "core/tests", "workspaces", "sessions"]
    REQUIRED_FILES = [
        "core/runtime/runtime_llm_provider.py",
        "core/runtime/runtime_autonomous_pipeline.py",
        "core/runtime/runtime_execution_graph.py",
        "core/runtime/runtime_task_state_machine.py",
        "umbra.py",
    ]

    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.getcwd()
        self.check_history = []

    def run_all_checks(self):
        report = HealthReport()
        self._check_directory_structure(report)
        self._check_required_files(report)
        self._check_python_version(report)
        self._check_disk_space(report)
        self._check_ollama_available(report)
        self._check_workspaces_dir(report)
        self.check_history.append(report.to_dict())
        return report

    def _check_directory_structure(self, report):
        for d in self.REQUIRED_DIRS:
            path = os.path.join(self.base_dir, d)
            if os.path.exists(path):
                report.add_check(f"dir:{d}", "pass", f"exists: {path}")
            else:
                os.makedirs(path, exist_ok=True)
                report.add_check(f"dir:{d}", "warn", f"created missing dir: {path}", "warn")

    def _check_required_files(self, report):
        for f in self.REQUIRED_FILES:
            path = os.path.join(self.base_dir, f)
            if os.path.exists(path):
                report.add_check(f"file:{f}", "pass")
            else:
                report.add_check(f"file:{f}", "fail", f"missing: {path}", "critical")

    def _check_python_version(self, report):
        major, minor = sys.version_info[:2]
        if major == 3 and minor >= 10:
            report.add_check("python_version", "pass", f"Python {major}.{minor}")
        elif major == 3 and minor >= 8:
            report.add_check("python_version", "warn", f"Python {major}.{minor} — 3.10+ recommended")
        else:
            report.add_check("python_version", "fail", f"Python {major}.{minor} — 3.8+ required", "critical")

    def _check_disk_space(self, report):
        try:
            stat = os.statvfs(self.base_dir) if hasattr(os, "statvfs") else None
            if stat:
                free_gb = (stat.f_bavail * stat.f_frsize) / (1024 ** 3)
                if free_gb > 2:
                    report.add_check("disk_space", "pass", f"{free_gb:.1f}GB free")
                elif free_gb > 0.5:
                    report.add_check("disk_space", "warn", f"Low disk: {free_gb:.1f}GB free", "warn")
                else:
                    report.add_check("disk_space", "fail", f"Critical disk: {free_gb:.1f}GB free", "critical")
            else:
                report.add_check("disk_space", "pass", "check skipped (Windows)")
        except Exception as e:
            report.add_check("disk_space", "warn", f"Could not check: {e}")

    def _check_ollama_available(self, report):
        import urllib.request
        try:
            with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as resp:
                report.add_check("ollama", "pass", "Ollama running at localhost:11434")
        except Exception:
            report.add_check("ollama", "warn", "Ollama not reachable — LLM calls will fail", "warn")

    def _check_workspaces_dir(self, report):
        ws_dir = os.path.join(self.base_dir, "workspaces")
        try:
            count = len(os.listdir(ws_dir)) if os.path.exists(ws_dir) else 0
            report.add_check("workspaces", "pass", f"{count} workspace(s) on disk")
        except Exception as e:
            report.add_check("workspaces", "warn", str(e))

    def get_history(self):
        return list(self.check_history)

    def quick_status(self):
        report = self.run_all_checks()
        return report.overall_status