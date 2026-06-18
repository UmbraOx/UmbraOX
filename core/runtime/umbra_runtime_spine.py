from core.runtime.umbra_generation_engine import UmbraGenerationEngine
from core.runtime.umbra_asset_store import UmbraAssetStore
from core.agents.boss_agent import BossAgent


class UmbraRuntimeSpine:
    """
    CENTRAL SYSTEM WIRING LAYER

    This connects:
    - BossAgent (planning)
    - GenerationEngine (execution)
    - AssetStore (memory/persistence)
    """

    def __init__(self, base_path="C:\\Umbra"):

        self.base_path = base_path

        # ----------------------
        # CORE SYSTEMS
        # ----------------------

        self.asset_store = UmbraAssetStore()
        self.generation_engine = UmbraGenerationEngine(self.asset_store)
        self.boss_agent = BossAgent(base_path)

    # ----------------------
    # MAIN EXECUTION ENTRY
    # ----------------------

    def run_task(self, task: dict):

        decision = self.boss_agent.bridge.analyze(task)

        if decision.get("action") == "generate":

            result = self.generation_engine.generate(task)

            return result

        return {
            "status": "queued",
            "reason": decision
        }

    # ----------------------
    # SYSTEM CYCLE
    # ----------------------

    def tick(self):

        cycle = self.boss_agent.run_cycle()

        next_task = self.boss_agent.execute_next()

        if next_task and next_task.get("status") != "idle":

            return self.run_task(next_task)

        return {
            "status": "idle",
            "cycle": cycle
        }