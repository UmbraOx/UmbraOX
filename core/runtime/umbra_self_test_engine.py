import subprocess


class UmbraSelfTestEngine:
    """
    Runs lightweight validation before ANY patch is applied.
    """

    def __init__(self, test_command="pytest -q"):
        self.test_command = test_command

    def run_tests(self) -> dict:

        try:
            result = subprocess.run(
                self.test_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout[-2000:],
                "error": result.stderr[-2000:]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }