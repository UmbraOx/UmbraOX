from core.runtime.pipeline_coordinator import (
    PipelineCoordinator
)


class UnifiedRuntimeEngine:

    def __init__(self):

        self.pipeline = PipelineCoordinator()

    def execute(self, objective):

        return self.pipeline.run(
            objective
        )