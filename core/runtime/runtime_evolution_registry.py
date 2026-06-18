from pathlib import Path


class EvolutionRegistry:
    """
    SINGLE SOURCE OF TRUTH FOR EVOLUTION SYSTEMS

    Prevents:
    - duplicate evolution engines
    - conflicting self-mod systems
    - runtime ambiguity
    """

    def __init__(self, root_dir: str):
        self.root = Path(root_dir)

        self.active_engines = {
            "evolver": "runtime_self_evolver",
            "repair": "runtime_self_repair_engine",
            "patch": "umbra_llm_patch_engine",
            "governor": "runtime_evolution_governor"
        }

    def get_engine(self, name: str):
        return self.active_engines.get(name)

    def list_engines(self):
        return self.active_engines

    def is_authorized(self, engine: str) -> bool:
        return engine in self.active_engines.values()