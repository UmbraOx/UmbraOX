import time
import threading


class AutonomousConstructionLoop:

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

        print("[CONSTRUCTION_LOOP] started")

    def loop(self):

        while self.running:

            print("[CONSTRUCTION_LOOP] idle")

            time.sleep(15)