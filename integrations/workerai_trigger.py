from core.runtime.umbra_runtime import UmbraRuntime


class WorkerAIUmbraTrigger:
    """
    Single entry point for WorkerAI → Umbra OS
    """

    def __init__(self, base_path: str = r"C:\Umbra", auto_mode: bool = False):
        self.runtime = UmbraRuntime(base_path, auto_mode=auto_mode)

    # ---------------------------
    # ONE-SHOT AUDIT (SAFE)
    # ---------------------------
    def run_audit(self):
        return self.runtime.boss.run_cycle()

    # ---------------------------
    # ONE STEP EVOLUTION
    # ---------------------------
    def run_step(self):
        return self.runtime.step()

    # ---------------------------
    # FULL AUTONOMY MODE
    # ---------------------------
    def run_autonomous(self, interval: int = 10):
        self.runtime.interval = interval
        self.runtime.run()