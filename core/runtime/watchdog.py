import threading
import time


class Watchdog:
    def __init__(self):
        self.running = False
        self.thread = None

    def _loop(self):
        while self.running:
            print("[WATCHDOG] runtime healthy")

            time.sleep(10)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("[WATCHDOG] started")