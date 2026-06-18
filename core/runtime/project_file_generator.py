import os


class ProjectFileGenerator:

    def write(
        self,
        path,
        content
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
        ) as file:

            file.write(content)

        return path