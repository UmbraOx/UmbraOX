import time
from datetime import datetime


class RuntimeDaemon:
    """
    Main Umbra background loop.
    Runs self-improvement + system checks periodically.
    """

    def __init__(self, self_improvement_loop, interval_seconds=300):
        self.loop = self_improvement_loop
        self.interval = interval_seconds
        self.running = False
        self.cycle_count = 0

    def start(self):
        self.running = True
        print("[UMBRA] Daemon started")

        while self.running:
            self.cycle()

            time.sleep(self.interval)

    def stop(self):
        self.running = False
        print("[UMBRA] Daemon stopped")

    def cycle(self):
        self.cycle_count += 1

        print(f"[UMBRA] Cycle {self.cycle_count} @ {datetime.now().isoformat()}")

        try:
            result = self.loop.run_cycle()

            if result is None:
                print("[UMBRA] No improvement targets found.")
            else:
                print("[UMBRA] Improvement cycle executed.")

        except Exception as e:
            print(f"[UMBRA] Cycle error: {e}")