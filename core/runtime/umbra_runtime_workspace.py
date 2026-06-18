from pathlib import Path


class UmbraRuntimeWorkspace:

    def initialize(self):

        directories = [
            "workspace",
            "workspace/modules",
            "workspace/snapshots",
            "workspace/logs",
            "workspace/projects"
        ]

        for directory in directories:

            Path(directory).mkdir(
                parents=True,
                exist_ok=True
            )

        return directories