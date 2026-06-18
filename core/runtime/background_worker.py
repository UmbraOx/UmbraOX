import time


class BackgroundWorker:
    def __init__(self, queue):
        self.queue = queue
        self.running = True

    def loop(self):
        while self.running:
            pending = self.queue.load()

            if pending:
                print(f"[BACKGROUND_WORKER] pending tasks: {len(pending)}")

            time.sleep(5)