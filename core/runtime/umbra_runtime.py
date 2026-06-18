from core.agents.boss_agent import BossAgent
import time


class UmbraRuntime:
    """
    Central execution runtime for Umbra OS
    Replaces ad-hoc WorkerAI triggering
    """

    def __init__(self, base_path: str, auto_mode: bool = False, interval: int = 10):
        self.boss = BossAgent(base_path, auto_mode=auto_mode)
        self.interval = interval
        self.running = False

    # ---------------------------
    # SINGLE STEP EXECUTION
    # ---------------------------
    def step(self):
        cycle = self.boss.run_cycle()
        task = self.boss.execute_next()

        return {
            "cycle": cycle,
            "task": task
        }

    # ---------------------------
    # CONTINUOUS LOOP
    # ---------------------------
    def run(self):
        self.running = True

        print("UMBRA RUNTIME STARTED")

        while self.running:
            result = self.step()

            print("\n--- UMBRA CYCLE ---")
            print(result["cycle"])

            if result["task"]["status"] != "idle":
                print("\n--- TASK PROPOSAL ---")
                print(result["task"]["diff"])

            time.sleep(self.interval)

    def stop(self):
        self.running = False