from pathlib import Path


class ExecutionPipeline:

    def execute(self, generated):

        written = []

        for item in generated:

            path = Path(item["path"])

            path.parent.mkdir(
                parents=True,
                exist_ok=True
            )

            path.write_text(
                item["content"],
                encoding="utf-8"
            )

            written.append(str(path))

        return written