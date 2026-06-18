from core.runtime.runtime_source_orchestrator import (
    RuntimeSourceOrchestrator
)


class RecursiveCodeGenerationEngine:

    def __init__(self):

        self.orchestrator = (
            RuntimeSourceOrchestrator()
        )

    def generate(
        self,
        objectives
    ):

        outputs = []

        for index, objective in enumerate(
            objectives,
            start=1
        ):

            class_name = (
                f"GeneratedModule{index}"
            )

            path = (
                f"generated/module_{index}.py"
            )

            output = (
                self.orchestrator
                .generate_module(
                    class_name,
                    path
                )
            )

            outputs.append(output)

        return outputs