import subprocess
import tempfile
import os

class SandboxRunner:
    """
    Executes code in isolated temporary environment.
    """

    def run_python(self, code: str):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
            f.write(code.encode("utf-8"))
            path = f.name

        try:
            result = subprocess.run(
                ["python", path],
                capture_output=True,
                text=True,
                timeout=5
            )

            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "code": result.returncode
            }

        finally:
            try:
                os.remove(path)
            except:
                pass


sandbox_runner = SandboxRunner()