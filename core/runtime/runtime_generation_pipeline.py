class RuntimeGenerationPipeline:

    def __init__(self):
        from core.runtime.runtime_generated_code import RuntimeGeneratedCode
        from core.runtime.runtime_file_writer import RuntimeFileWriter
        from core.runtime.runtime_removable_registry import RuntimeRemovableRegistry

        self.generator = RuntimeGeneratedCode()
        self.writer = RuntimeFileWriter()
        self.removable = RuntimeRemovableRegistry()

    def generate(self, domains):
        written = []
        generated = []

        for domain in domains:
            module = self.generator.build(domain)
            generated.append(module)

            self.writer.write(
                module["path"],
                module["content"]
            )

            written.append(module["path"])

            self.removable.mark(
                module["path"],
                reason="auto_generated"
            )

        return {
            "generated": generated,
            "written": written
        }