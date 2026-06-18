import threading
import time


class RuntimeCoordinator:
    def __init__(self):
        self.running = False
        self.threads = []

    def register(self, target, name="worker"):
        thread = threading.Thread(target=target, daemon=True)
        thread.name = name
        self.threads.append(thread)

    def start(self):
        self.running = True

        for thread in self.threads:
            thread.start()

        print("[COORDINATOR] started")

    def stop(self):
        self.running = False
        print("[COORDINATOR] stopping")

    def heartbeat(self):
        while self.running:
            print("[COORDINATOR] heartbeat")
            time.sleep(10)