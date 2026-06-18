from pathlib import Path
from datetime import datetime
from datetime import UTC

import shutil
import uuid


class RuntimeBackupSystem:

    def __init__(self):

        self.root = Path(
            "runtime_backups"
        )

        self.root.mkdir(
            exist_ok=True
        )

    def backup_project(self):

        timestamp = (
            datetime.now(UTC)
            .strftime("%Y%m%d_%H%M%S")
        )

        unique_id = (
            uuid.uuid4().hex[:8]
        )

        destination = (
            self.root /
            f"backup_{timestamp}_{unique_id}"
        )

        shutil.copytree(
            ".",
            destination,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                "*.pyc",
                "venv",
                ".git",
                "runtime_backups"
            )
        )

        return {
            "success": True,
            "path": str(destination)
        }