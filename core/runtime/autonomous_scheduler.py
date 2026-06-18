import time


class AutonomousScheduler:
    def __init__(self):
        self.jobs = []
        self.running = True

    def add_job(self, name, callback):
        self.jobs.append({
            "name": name,
            "callback": callback
        })

        print(f"[SCHEDULER] job added: {name}")

    def loop(self):
        while self.running:
            for job in self.jobs:
                try:
                    job["callback"]()
                except Exception as e:
                    print(f"[SCHEDULER ERROR] {e}")

            time.sleep(15)