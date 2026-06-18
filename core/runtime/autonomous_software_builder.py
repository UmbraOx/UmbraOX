from core.runtime.recursive_code_generation_engine import (
    RecursiveCodeGenerationEngine
)


class AutonomousSoftwareBuilder:

    def __init__(self):

        self.engine = (
            RecursiveCodeGenerationEngine()
        )

    def build(
        self,
        objectives
    ):

        return self.engine.generate(
            objectives
        )