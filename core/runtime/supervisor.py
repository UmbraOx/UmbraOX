import threading
import time


class Supervisor:
    def __init__(self):
        self.running = False
        self.thread = None

    def _loop(self):
        while self.running:
            print("[SUPERVISOR] monitoring runtime")

            time.sleep(8)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("[SUPERVISOR] started")