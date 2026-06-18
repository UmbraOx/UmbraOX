from core.runtime.runtime_unified_orchestrator import RuntimeUnifiedOrchestrator


class RuntimeSystemInitializer:
    """
    SINGLE ENTRY POINT TO START UMBRA
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.system = RuntimeUnifiedOrchestrator(base_path)

    # -------------------------
    # FULL BOOT
    # -------------------------
    def start(self):
        return self.system.start()

    # -------------------------
    # SINGLE CYCLE RUN
    # -------------------------
    def run_once(self):
        return self.system.run_cycle()