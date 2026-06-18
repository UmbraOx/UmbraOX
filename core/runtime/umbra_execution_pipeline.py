from core.runtime.runtime_code_synthesizer import (
    RuntimeCodeSynthesizer
)

from core.runtime.runtime_file_writer import (
    RuntimeFileWriter
)


class UmbraExecutionPipeline:

    def __init__(self):
        self.synthesizer = (
            RuntimeCodeSynthesizer()
        )

        self.writer = (
            RuntimeFileWriter()
        )

    def execute(
        self,
        objective
    ):
        generated = (
            self.synthesizer.synthesize(
                objective
            )
        )

        self.writer.write(
            generated["path"],
            generated["content"]
        )

        return generated