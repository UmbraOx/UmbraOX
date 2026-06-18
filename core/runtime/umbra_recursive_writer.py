from core.runtime.runtime_file_writer import (
    RuntimeFileWriter
)


class UmbraRecursiveWriter:

    def __init__(self):
        self.writer = (
            RuntimeFileWriter()
        )

    def write_module(
        self,
        path,
        content
    ):
        self.writer.write(
            path,
            content
        )

        return {
            "path": path,
            "written": True
        }