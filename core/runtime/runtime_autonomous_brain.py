from core.runtime.runtime_command_processor import RuntimeCommandProcessor
from core.runtime.runtime_task_planner import RuntimeTaskPlanner
from core.runtime.runtime_execution_pipeline import RuntimeExecutionPipeline
from core.runtime.runtime_goal_orchestrator import RuntimeGoalOrchestrator


class RuntimeAutonomousBrain:
    def __init__(self):
        self.processor = RuntimeCommandProcessor()
        self.planner = RuntimeTaskPlanner()
        self.pipeline = RuntimeExecutionPipeline()
        self.orchestrator = RuntimeGoalOrchestrator()

    def execute_objective(self, objective: str):
        processed = self.processor.process(objective)

        self.orchestrator.register_goal(objective)

        plan = self.planner.create_plan(objective)

        execution = self.pipeline.run(plan)

        return {
            "processed": processed,
            "plan": plan,
            "execution": execution,
            "status": "success"
        }