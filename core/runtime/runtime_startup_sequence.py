from core.runtime.umbra_runtime_kernel import UmbraRuntimeKernel

class RuntimeStartupSequence:
    """
    Deterministic boot sequence for Umbra OS
    """

    def __init__(self, base_path: str):
        self.base_path = base_path
        self.kernel = UmbraRuntimeKernel(base_path)

    # -------------------------
    # LOAD ORDER
    # -------------------------
    def build_modules(self):
        """
        Import and construct runtime modules safely
        """

        # Lazy imports prevent circular dependency failure
        from core.runtime.runtime_self_repair_engine import RuntimeSelfRepairEngine
        from core.runtime.runtime_task_scheduler import RuntimeTaskScheduler
        from core.runtime.runtime_system_monitor import RuntimeSystemMonitor
        from core.runtime.runtime_self_evolution_engine import RuntimeSelfEvolutionEngine

        return {
            "repair_engine": RuntimeSelfRepairEngine(self.base_path),
            "task_scheduler": RuntimeTaskScheduler(),
            "system_monitor": RuntimeSystemMonitor(),
            "self_evolution_engine": RuntimeSelfEvolutionEngine(self.base_path)
        }

    # -------------------------
    # START SYSTEM
    # -------------------------
    def start(self):
        modules = self.build_modules()
        self.kernel.bootstrap(modules)
        self.kernel.start_system()