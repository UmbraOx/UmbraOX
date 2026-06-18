# core/runtime/safety_gate.py


class SafetyGate:

    def __init__(self):

        self.blocked_paths = [
            "venv",
            "__pycache__",
            ".git",
            "runtime_snapshots"
        ]

        self.blocked_keywords = [
            "os.remove",
            "shutil.rmtree",
            "subprocess",
            "eval(",
            "exec("
        ]

    # -------------------------------------------------
    # PATH CHECK
    # -------------------------------------------------

    def validate_path(self, path):

        lowered = path.lower()

        for blocked in self.blocked_paths:

            if blocked.lower() in lowered:

                print(f"[SAFETY] blocked path: {path}")

                return False

        return True

    # -------------------------------------------------
    # CONTENT CHECK
    # -------------------------------------------------

    def validate_content(self, content):

        lowered = content.lower()

        for keyword in self.blocked_keywords:

            if keyword.lower() in lowered:

                print(f"[SAFETY] blocked keyword: {keyword}")

                return False

        return True

    # -------------------------------------------------
    # FULL VALIDATION
    # -------------------------------------------------

    def validate_patch(self, path, content):

        if not self.validate_path(path):
            return False

        if not self.validate_content(content):
            return False

        return True