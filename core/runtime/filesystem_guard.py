import os


class FilesystemGuard:
    """
    Prevents dangerous filesystem writes.
    """

    BLOCKED = [
        "C:/Windows",
        "C:/Program Files",
        "/bin",
        "/usr",
    ]

    def validate(self, path):

        normalized = path.replace(
            "\\",
            "/"
        )

        for blocked in self.BLOCKED:

            if normalized.startswith(blocked):

                raise Exception(
                    f"blocked path: {path}"
                )

        return True

    def validate_bundle(self, bundle):

        for path in bundle["files"]:

            self.validate(path)

        return True