from core.runtime.code_generation_engine import CodeGenerationEngine


class AutonomousCodegenPipeline:

    def __init__(self):

        self.engine = CodeGenerationEngine()

    def generate(self, prompt, proposals):

        generated = []

        for proposal in proposals:

            result = self.engine.generate(
                prompt,
                proposal
            )

            if result:
                generated.extend(result)

        return generated