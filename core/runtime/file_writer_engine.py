import os


class FileWriterEngine:

    def write(
        self,
        path,
        code
    ):

        directory = os.path.dirname(path)

        if directory:

            os.makedirs(
                directory,
                exist_ok=True
            )

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(code)

        print(
            f"[FILE WRITTEN] {path}"
        )

        return path