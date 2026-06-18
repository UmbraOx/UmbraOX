from core.runtime.file_writer_engine import (
    FileWriterEngine
)

from core.runtime.generated_asset_registry import (
    GeneratedAssetRegistry
)


class GeneratedProjectBuilder:

    def __init__(self):

        self.writer = (
            FileWriterEngine()
        )

        self.registry = (
            GeneratedAssetRegistry()
        )

    def build(
        self,
        generated
    ):

        written = []

        for item in generated:

            path = item["path"]
            code = item["code"]

            self.writer.write(
                path,
                code
            )

            self.registry.register(
                item
            )

            written.append(path)

        return written