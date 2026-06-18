import threading
import time


class AutonomyLoop:

    def __init__(self):
        self.running = False
        self.thread = None

    def _loop(self):
        while self.running:
            print("[AUTONOMY_LOOP] idle")
            time.sleep(5)

    def start(self):
        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("[AUTONOMY_LOOP] started background thread")

    def stop(self):
        self.running = False


_autonomy_instance = AutonomyLoop()


def start_autonomy_loop():
    _autonomy_instance.start()


def stop_autonomy_loop():
    _autonomy_instance.stop()