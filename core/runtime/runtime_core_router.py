class RuntimeCoreRouter:
    """
    Central coordination layer for Umbra runtime systems.

    This is NOT an AI. It is a deterministic orchestrator.
    """

    def __init__(self, pipeline, analyzer, improvement_loop, validator=None):
        self.pipeline = pipeline
        self.analyzer = analyzer
        self.improvement_loop = improvement_loop
        self.validator = validator

    # ---------------------------------------------------------
    # MAIN CYCLE
    # ---------------------------------------------------------
    def run_cycle(self):
        plan = self.improvement_loop.analyze_and_plan()

        if not plan.targets:
            return {
                "status": "idle",
                "reason": "no_targets"
            }

        executed = self.improvement_loop.execute_plan(plan)

        validation_result = None
        if self.validator:
            validation_result = self.validator.validate_all_python_files(
                "C:\\Umbra"
            )

        return {
            "status": "completed",
            "plan": plan.to_dict(),
            "validation": validation_result
        }

    # ---------------------------------------------------------
    # SAFE ENTRY POINTS
    # ---------------------------------------------------------
    def analyze_only(self):
        return self.analyzer.get_module_summary()

    def plan_only(self):
        return self.improvement_loop.analyze_and_plan().to_dict()