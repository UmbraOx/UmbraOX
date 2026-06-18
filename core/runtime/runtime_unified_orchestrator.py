from core.agents.boss_agent import BossAgent
from core.runtime.umbra_runtime_kernel import UmbraRuntimeKernel
from core.runtime.runtime_self_evolver import RuntimeSelfEvolver
from core.runtime.runtime_evolution_governor import EvolutionGovernor


class RuntimeUnifiedOrchestrator:
    """
    SINGLE CONTROL PLANE FOR UMBRA

    Connects:
    - BossAgent (decision layer)
    - Kernel (execution loop)
    - Evolver (self-improvement)
    - Governor (safety)
    """

    def __init__(self, base_path: str):
        self.base_path = base_path

        self.boss = BossAgent(base_path, auto_mode=False)
        self.kernel = UmbraRuntimeKernel(base_path)
        self.evolver = RuntimeSelfEvolver(base_path, auto_apply=False)
        self.governor = EvolutionGovernor()

    # -------------------------
    # SYSTEM BOOT
    # -------------------------
    def bootstrap(self):
        modules = self._build_modules()
        self.kernel.bootstrap(modules)

    def _build_modules(self):
        return {
            "boss": self.boss,
            "evolver": self.evolver,
            "governor": self.governor
        }

    # -------------------------
    # FULL SYSTEM RUN LOOP
    # -------------------------
    def run_cycle(self):
        """
        Orchestrated Umbra cycle:
        1. Boss scans & prioritizes
        2. Evolver proposes improvements
        3. Governor validates safety
        4. Kernel executes cycle tick
        """

        audit = self.boss.run_cycle()
        evolution = self.evolver.run_cycle(limit=10)

        safe_results = []

        for item in evolution.get("results", []):
            file_path = item.get("file")

            if not file_path:
                continue

            allowed = self.governor.allow_patch(file_path)

            safe_results.append({
                "file": file_path,
                "allowed": allowed,
                "valid": item.get("valid"),
                "diff": item.get("diff"),
                "applied": item.get("applied", False)
            })

        return {
            "audit": audit,
            "evolution": evolution,
            "safe_results": safe_results
        }

    # -------------------------
    # START SYSTEM
    # -------------------------
    def start(self):
        self.bootstrap()
        return self.run_cycle()