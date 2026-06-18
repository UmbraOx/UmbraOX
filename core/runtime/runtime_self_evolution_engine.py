from core.runtime.runtime_gap_analyzer import (
    RuntimeGapAnalyzer
)

from core.runtime.runtime_self_evolution_planner import (
    RuntimeSelfEvolutionPlanner
)

from core.runtime.runtime_prompt_orchestrator import (
    RuntimePromptOrchestrator
)

from core.runtime.runtime_capability_registry import (
    RuntimeCapabilityRegistry
)


class RuntimeSelfEvolutionEngine:

    def __init__(self):

        self.gap_analyzer = (
            RuntimeGapAnalyzer()
        )

        self.planner = (
            RuntimeSelfEvolutionPlanner()
        )

        self.orchestrator = (
            RuntimePromptOrchestrator()
        )

        self.registry = (
            RuntimeCapabilityRegistry()
        )

    def evolve(self):

        capabilities = (
            self.registry.get_capabilities()
        )

        analysis = (
            self.gap_analyzer.analyze(
                capabilities
            )
        )

        if analysis["complete"]:

            return {
                "success": True,
                "message": "runtime_complete"
            }

        plan = (
            self.planner.build_plan(
                analysis["missing"]
            )
        )

        results = []

        for task in plan:

            try:

                result = (
                    self.orchestrator.execute(
                        task
                    )
                )

                results.append(
                    {
                        "task": task,
                        "result": result,
                        "success": True
                    }
                )

            except Exception as e:

                results.append(
                    {
                        "task": task,
                        "success": False,
                        "error": str(e)
                    }
                )

        return {
            "success": True,
            "analysis": analysis,
            "plan": plan,
            "results": results
        }