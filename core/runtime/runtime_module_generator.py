from core.runtime.code_generation_engine import (
    CodeGenerationEngine
)


class RuntimeModuleGenerator:

    def __init__(self):

        self.engine = (
            CodeGenerationEngine()
        )

    def build(
        self,
        module_name
    ):

        return self.engine.generate_module(
            module_name,
            "runtime"
        )