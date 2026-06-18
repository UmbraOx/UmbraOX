class RuntimeSystemController:
    """
    Global coordination hub for Umbra runtime.
    """

    def __init__(self, bootstrap, cleanup_engine, tracker):
        self.bootstrap = bootstrap
        self.cleanup = cleanup_engine
        self.tracker = tracker

    def start_system(self):
        self.bootstrap.start()

    def run_cleanup(self):
        return self.cleanup.cleanup_all()

    def status(self):
        return {
            "tracked_files": len(self.tracker.list()),
        }