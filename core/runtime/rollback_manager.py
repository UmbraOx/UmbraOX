import os
import shutil
from datetime import datetime


class RollbackManager:

    def __init__(self):

        self.root = "./backups"

        os.makedirs(
            self.root,
            exist_ok=True
        )

    def create_checkpoint(self, target):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        checkpoint = os.path.join(
            self.root,
            timestamp
        )

        os.makedirs(
            checkpoint,
            exist_ok=True
        )

        if os.path.exists(target):

            name = os.path.basename(target)

            destination = os.path.join(
                checkpoint,
                name
            )

            if os.path.isdir(target):

                shutil.copytree(
                    target,
                    destination,
                    dirs_exist_ok=True
                )

            else:

                shutil.copy2(
                    target,
                    destination
                )

        print(
            f"[ROLLBACK] checkpoint created: {checkpoint}"
        )

        return checkpoint