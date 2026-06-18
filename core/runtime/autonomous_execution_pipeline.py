from core.runtime.runtime_pipeline_manager import RuntimePipelineManager
from core.runtime.runtime_execution_controller import RuntimeExecutionController


class AutonomousExecutionPipeline:

    def __init__(self):
        self.pipeline_manager = RuntimePipelineManager()
        self.controller = RuntimeExecutionController()

    def run(self, objective):
        pipeline = self.pipeline_manager.build_pipeline(objective)

        results = self.controller.execute(pipeline)

        return {
            "objective": objective,
            "pipeline": pipeline,
            "results": results
        }