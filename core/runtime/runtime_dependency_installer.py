import sys
import importlib
from datetime import datetime


class InstallResult:

    def __init__(self, package, success, message, already_installed=False):
        self.package = package
        self.success = success
        self.message = message
        self.already_installed = already_installed
        self.installed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "package": self.package,
            "success": self.success,
            "message": self.message,
            "already_installed": self.already_installed,
            "installed_at": self.installed_at,
        }


class RuntimeDependencyInstaller:
    """
    Autonomous package and environment management.
    Checks if packages are importable before installing.
    Uses subprocess executor if available, otherwise falls back to pip directly.
    Tracks install history and provides rollback list.
    """

    # Packages that must never be auto-installed
    BLOCKED_PACKAGES = [
        "os", "sys", "subprocess", "shutil", "socket",
        "ctypes", "multiprocessing",
    ]

    def __init__(self, subprocess_executor=None):
        self.executor = subprocess_executor
        self.install_history = []
        self.installed_this_session = []

    def is_installed(self, package_name):
        """Check if a package is importable."""
        # Normalize package name for import check
        import_name = package_name.replace("-", "_").split("==")[0].split(">=")[0].strip()
        try:
            importlib.import_module(import_name)
            return True
        except ImportError:
            return False

    def install(self, package, force=False):
        """
        Install a package if not already present.
        Returns InstallResult.
        """
        base_name = package.split("==")[0].split(">=")[0].strip()

        if base_name in self.BLOCKED_PACKAGES:
            result = InstallResult(package, False, f"Blocked: {base_name} is a stdlib module")
            self.install_history.append(result.to_dict())
            return result

        if not force and self.is_installed(base_name):
            result = InstallResult(package, True, f"Already installed: {base_name}", already_installed=True)
            self.install_history.append(result.to_dict())
            return result

        if self.executor:
            exec_result = self.executor.execute_pip_install(package)
            success = exec_result.success
            message = exec_result.stdout if success else exec_result.stderr
        else:
            # Fallback: direct pip via subprocess
            import subprocess
            proc = subprocess.run(
                [sys.executable, "-m", "pip", "install", package],
                capture_output=True, text=True, timeout=60
            )
            success = proc.returncode == 0
            message = proc.stdout if success else proc.stderr

        result = InstallResult(package, success, message[:300])
        self.install_history.append(result.to_dict())
        if success:
            self.installed_this_session.append(base_name)
        return result

    def install_many(self, packages):
        """Install a list of packages. Returns list of InstallResults."""
        return [self.install(p) for p in packages]

    def ensure(self, package):
        """Install only if not already present. Silent if already installed."""
        return self.install(package, force=False)

    def check_requirements(self, requirements):
        """
        Given a list of package names, return which are missing.
        """
        missing = []
        for pkg in requirements:
            base = pkg.split("==")[0].split(">=")[0].strip()
            if not self.is_installed(base):
                missing.append(pkg)
        return missing

    def get_history(self):
        return list(self.install_history)

    def get_session_installs(self):
        return list(self.installed_this_session)

    def uninstall_session_installs(self):
        """Rollback: uninstall everything installed this session."""
        results = []
        for pkg in self.installed_this_session:
            if self.executor:
                r = self.executor.execute(f'"{sys.executable}" -m pip uninstall -y {pkg}')
            else:
                import subprocess
                proc = subprocess.run(
                    [sys.executable, "-m", "pip", "uninstall", "-y", pkg],
                    capture_output=True, text=True, timeout=30
                )
                r = type("R", (), {"success": proc.returncode == 0, "stdout": proc.stdout})()
            results.append({"package": pkg, "success": r.success})
        self.installed_this_session.clear()
        return results