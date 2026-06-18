from core.runtime.objective_pipeline import (
    ObjectivePipeline
)

from core.runtime.proposal_pipeline import (
    ProposalPipeline
)

from core.runtime.generation_pipeline import (
    GenerationPipeline
)

from core.runtime.validation_pipeline import (
    ValidationPipeline
)

from core.runtime.execution_pipeline import (
    ExecutionPipeline
)

from core.runtime.memory_pipeline import (
    MemoryPipeline
)

from core.runtime.runtime_execution_context import (
    RuntimeExecutionContext
)


class PipelineCoordinator:

    def __init__(self):

        self.objectives = ObjectivePipeline()

        self.proposals = ProposalPipeline()

        self.generation = GenerationPipeline()

        self.validation = ValidationPipeline()

        self.execution = ExecutionPipeline()

        self.memory = MemoryPipeline()

    def run(self, objective):

        context = RuntimeExecutionContext()

        context.set(
            "objective",
            objective
        )

        domains = self.objectives.process(
            objective
        )

        context.set(
            "domains",
            domains
        )

        proposals = self.proposals.generate(
            domains
        )

        context.set(
            "proposals",
            proposals
        )

        generated = self.generation.generate(
            proposals
        )

        context.set(
            "generated",
            generated
        )

        validated = self.validation.validate(
            generated
        )

        context.set(
            "validated",
            validated
        )

        if validated:

            written = self.execution.execute(
                generated
            )

            context.set(
                "written",
                written
            )

            context.set(
                "executed",
                True
            )

        self.memory.write(
            context.export()
        )

        context.set(
            "memory_written",
            True
        )

        return context.export()