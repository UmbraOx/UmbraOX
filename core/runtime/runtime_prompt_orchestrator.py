from datetime import datetime
from datetime import UTC

from core.runtime.runtime_extension_pipeline import (
    RuntimeExtensionPipeline
)

from core.runtime.runtime_persistent_brain import (
    RuntimePersistentBrain
)

from core.runtime.runtime_goal_engine import (
    RuntimeGoalEngine
)

from core.runtime.runtime_module_registry import (
    RuntimeModuleRegistry
)

from core.runtime.runtime_project_graph import (
    RuntimeProjectGraph
)

from core.runtime.runtime_dependency_graph import (
    RuntimeDependencyGraph
)


class RuntimePromptOrchestrator:

    def __init__(self):

        self.pipeline = (
            RuntimeExtensionPipeline()
        )

        self.brain = (
            RuntimePersistentBrain()
        )

        self.goals = (
            RuntimeGoalEngine()
        )

        self.registry = (
            RuntimeModuleRegistry()
        )

        self.registry.discover_generated_modules()

        self.graph = (
            RuntimeProjectGraph()
        )

        self.dependency_engine = (
            RuntimeDependencyGraph()
        )

    def execute(
        self,
        prompt
    ):

        session = {
            "timestamp": (
                datetime.now(UTC).isoformat()
            ),
            "prompt": prompt
        }

        expanded = (
            self.goals.expand(prompt)
        )

        for goal in expanded:

            self.graph.add_node(
                goal
            )

        self.brain.remember(
            {
                "prompt": prompt,
                "expanded": expanded
            }
        )

        execution_results = []

        for goal in expanded:

            result = (
                self.pipeline.execute(
                    goal
                )
            )

            dependencies = (
                self.dependency_engine
                .infer_dependencies(
                    goal
                )
            )

            self.graph.record_event(
                {
                    "goal": goal,
                    "dependencies": dependencies
                }
            )

            execution_results.append(
                {
                    "goal": goal,
                    "dependencies": dependencies,
                    "result": result
                }
            )

        dependency_map = (
            self.dependency_engine
            .build_dependency_map()
        )

        return {
            "session": session,
            "expanded_goals": expanded,
            "execution": execution_results,
            "dependency_map": dependency_map,
            "graph": (
                self.graph.get_graph()
            ),
            "history": (
                self.graph.get_history()
            ),
            "memory_size": len(
                self.brain.load()
            )
        }