import time


class RuntimeWatchdog:
    """
    FINAL SAFETY GATE

    Stops runaway execution, protects self-mod engine
    """

    def __init__(self, kernel=None, timeout=8):
        self.kernel = kernel
        self.timeout = timeout
        self.last_ok = time.time()

    # -----------------------
    # HEARTBEAT
    # -----------------------
    def tick(self):
        self.last_ok = time.time()

    # -----------------------
    # HEALTH CHECK
    # -----------------------
    def healthy(self):
        return (time.time() - self.last_ok) < self.timeout

    # -----------------------
    # EMERGENCY STOP
    # -----------------------
    def emergency_stop(self):
        if self.kernel:
            self.kernel.halt()

    # -----------------------
    # RECOVERY
    # -----------------------
    def recover(self):
        if self.kernel:
            self.kernel.resume()
        self.tick()