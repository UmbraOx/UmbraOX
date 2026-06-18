from core.runtime.runtime_self_evolver import RuntimeSelfEvolver
from core.runtime.runtime_evolution_governor import EvolutionGovernor
from core.runtime.runtime_evolution_registry import EvolutionRegistry


class EvolutionBootstrap:
    """
    BOOTSTRAP LAYER FOR UMBRA EVOLUTION SYSTEM

    This is the correct entry point for startup wiring.
    """

    def __init__(self, root_dir: str):
        self.root_dir = root_dir

        self.registry = EvolutionRegistry(root_dir)
        self.governor = EvolutionGovernor()
        self.evolver = RuntimeSelfEvolver(root_dir)

    # -------------------------
    # SAFE EVOLUTION CYCLE
    # -------------------------
    def run(self, auto_apply: bool = False):
        report = self.evolver.run_cycle()

        safe_results = []

        for item in report.get("results", []):
            file_path = item.get("file")

            if not file_path:
                continue

            allowed = self.governor.allow_patch(file_path)

            safe_results.append({
                "file": file_path,
                "allowed": allowed,
                "valid": item.get("valid"),
                "applied": item.get("applied", False)
            })

        return {
            "report": report,
            "governor": self.governor.status(),
            "safe_results": safe_results
        }