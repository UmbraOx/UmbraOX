from core.runtime.umbra_self_repair_core import UmbraSelfRepairCore


class UmbraBridge:
    """
    Connects WorkerAI to Umbra Self-Repair System.
    This is the control surface between agent orchestration and runtime evolution.
    """

    def __init__(self, project_root: str):
        self.engine = UmbraSelfRepairCore(project_root)

    # -----------------------------------
    # MAIN ENTRY POINT
    # -----------------------------------

    def run_full_audit(self):
        """
        WorkerAI triggers a full Umbra scan + reasoning + plan.
        """
        print("\n[WorkerAI] Triggering Umbra full system audit...\n")
        return self.engine.run_scan()

    # -----------------------------------
    # FUTURE HOOK (LLM PATCH LAYER)
    # -----------------------------------

    def propose_self_improvement(self, context: dict):
        """
        Placeholder hook for LLM-driven evolution.
        Will later connect to diff engine.
        """
        return {
            "status": "not_implemented",
            "message": "LLM patch engine not yet wired"
        }