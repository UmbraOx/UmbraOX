import threading
import time


class RuntimeDaemonLoop:

    def __init__(self):
        self.running = False

    def start(self):
        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.loop,
            daemon=True
        )

        thread.start()

        print(
            "[RUNTIME_DAEMON] started"
        )

    def loop(self):
        while self.running:
            print(
                "[RUNTIME_DAEMON] heartbeat"
            )

            time.sleep(5)