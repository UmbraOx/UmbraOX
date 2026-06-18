import os

from core.runtime.filesystem_guard import (
    FilesystemGuard
)


class PatchDeployer:

    def __init__(self):

        self.guard = FilesystemGuard()

    def deploy(self, bundle):

        self.guard.validate_bundle(
            bundle
        )

        deployed = []

        for path, content in bundle["files"].items():

            directory = os.path.dirname(path)

            os.makedirs(
                directory,
                exist_ok=True
            )

            with open(
                path,
                "w",
                encoding="utf-8"
            ) as f:

                f.write(content)

            deployed.append(path)

            print(
                f"[PATCH] deployed: {path}"
            )

        return deployed