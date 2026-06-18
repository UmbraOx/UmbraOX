import threading
import time


class UmbraObjectiveLoop:

    def __init__(self):
        self.running = False

    def start(
        self,
        callback
    ):
        if self.running:
            return

        self.running = True

        thread = threading.Thread(
            target=self.loop,
            args=(callback,),
            daemon=True
        )

        thread.start()

    def loop(
        self,
        callback
    ):
        while self.running:
            callback()

            time.sleep(5)