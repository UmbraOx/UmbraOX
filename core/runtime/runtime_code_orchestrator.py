from core.runtime.code_generation_engine import CodeGenerationEngine


class RuntimeCodeOrchestrator:

    def __init__(self):

        self.generator = CodeGenerationEngine()

    def build(self, proposal):

        return self.generator.generate(proposal)