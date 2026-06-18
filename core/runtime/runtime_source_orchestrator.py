from core.runtime.source_code_synthesizer import (
    SourceCodeSynthesizer
)

from core.runtime.project_file_generator import (
    ProjectFileGenerator
)


class RuntimeSourceOrchestrator:

    def __init__(self):

        self.synthesizer = (
            SourceCodeSynthesizer()
        )

        self.writer = (
            ProjectFileGenerator()
        )

    def generate_module(
        self,
        class_name,
        output_path
    ):

        source = (
            self.synthesizer
            .synthesize_class(
                class_name
            )
        )

        self.writer.write(
            output_path,
            source
        )

        return output_path