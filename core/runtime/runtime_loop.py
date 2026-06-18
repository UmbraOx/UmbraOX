import threading
import time


class RuntimeLoop:

    def __init__(
        self,
        executor=None,
        router=None,
        planner=None
    ):
        self.executor = executor
        self.router = router
        self.planner = planner

        self.running = False
        self.thread = None

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self._loop,
            daemon=True
        )

        self.thread.start()

        print("[RUNTIME_LOOP] started")

    def stop(self):

        self.running = False

    def _loop(self):

        while self.running:

            print("[RUNTIME_LOOP] idle")

            time.sleep(5)