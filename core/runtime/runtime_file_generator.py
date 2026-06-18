from pathlib import Path


class RuntimeFileGenerator:

    def generate(
        self,
        path,
        content
    ):

        file_path = Path(path)

        file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        return str(file_path)