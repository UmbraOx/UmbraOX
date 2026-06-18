class ShutdownManager:
    def __init__(self):
        self.shutdown_requested = False

    def request_shutdown(self):
        self.shutdown_requested = True
        print("[SHUTDOWN] requested")

    def should_shutdown(self):
        return self.shutdown_requested