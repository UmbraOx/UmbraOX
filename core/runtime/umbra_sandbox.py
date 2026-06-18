import subprocess
import tempfile
from pathlib import Path


class UmbraSandbox:
    """
    Safe execution environment for patched code validation
    """

    def test_run(self, file_path: str):
        try:
            result = subprocess.run(
                ["python", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.decode(),
                "stderr": result.stderr.decode()
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }