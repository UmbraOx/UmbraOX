import datetime


class RuntimeUmbraCore:
    """
    Unified control layer for Umbra runtime.

    This is the single orchestration entrypoint.
    It does NOT replace systems — it coordinates them.
    """

    def __init__(self, analyzer=None, improvement_loop=None, repair_engine=None, pipeline=None):
        self.analyzer = analyzer
        self.improvement_loop = improvement_loop
        self.repair_engine = repair_engine
        self.pipeline = pipeline

        self.last_state = {}
        self.history = []

    # ----------------------------
    # FULL SYSTEM CYCLE
    # ----------------------------

    def run_cycle(self, input_data=None):
        """
        Executes full Umbra reasoning cycle:
        analyze → improve → repair → execute
        """

        state = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "analysis": None,
            "plan": None,
            "repair": None,
            "execution": None,
        }

        # 1. ANALYZE
        if self.analyzer:
            if hasattr(self.analyzer, "get_module_summary"):
                state["analysis"] = self.analyzer.get_module_summary()
            elif hasattr(self.analyzer, "scan_modules"):
                self.analyzer.scan_modules()
                state["analysis"] = self.analyzer.get_module_summary()

        # 2. IMPROVEMENT PLAN
        if self.improvement_loop:
            if hasattr(self.improvement_loop, "analyze_and_plan"):
                state["plan"] = self.improvement_loop.analyze_and_plan()
            elif hasattr(self.improvement_loop, "analyze"):
                state["plan"] = self.improvement_loop.analyze(state["analysis"])

        # 3. REPAIR (only if available)
        if self.repair_engine and state.get("analysis"):
            try:
                state["repair"] = self.repair_engine.repair(Exception("runtime_check"))
            except Exception as e:
                state["repair"] = {"error": str(e)}

        # 4. EXECUTION PIPELINE
        if self.pipeline:
            try:
                if hasattr(self.pipeline, "run"):
                    state["execution"] = self.pipeline.run([])
                else:
                    state["execution"] = {"status": "no_run_method"}
            except Exception as e:
                state["execution"] = {"error": str(e)}

        self.last_state = state
        self.history.append(state)

        return state

    # ----------------------------
    # INTROSPECTION
    # ----------------------------

    def get_last_state(self):
        return self.last_state

    def get_history(self):
        return self.history