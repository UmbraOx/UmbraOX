from core.runtime.runtime_extension_pipeline import (
    RuntimeExtensionPipeline
)

from core.runtime.runtime_persistent_brain import (
    RuntimePersistentBrain
)

from core.runtime.runtime_goal_engine import (
    RuntimeGoalEngine
)


class RuntimePromptOrchestrator:

    def __init__(self):

        self.pipeline = RuntimeExtensionPipeline()

        self.brain = RuntimePersistentBrain()

        self.goals = RuntimeGoalEngine()

    def execute(
        self,
        prompt
    ):

        expanded = self.goals.expand(
            prompt
        )

        self.brain.remember(
            {
                "prompt": prompt,
                "expanded": expanded
            }
        )

        execution = []

        for goal in expanded:

            result = self.pipeline.execute(
                goal
            )

            execution.append(result)

        return {
            "prompt": prompt,
            "expanded_goals": expanded,
            "execution": execution,
            "memory_size": len(
                self.brain.load()
            )
        }