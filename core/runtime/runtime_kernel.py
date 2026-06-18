import time
import threading


class RuntimeKernel:
    """
    FINAL EXECUTION KERNEL

    Responsibilities:
    - heartbeat control
    - execution gating
    - system lifecycle
    """

    def __init__(self):
        self.running = False
        self.last_tick = time.time()
        self.halted = False

    # -----------------------
    # START
    # -----------------------
    def start(self):
        if self.running:
            return

        self.running = True

        def loop():
            while self.running:

                if self.halted:
                    time.sleep(1)
                    continue

                self.last_tick = time.time()
                time.sleep(0.5)

        threading.Thread(target=loop, daemon=True).start()

    # -----------------------
    # STOP
    # -----------------------
    def stop(self):
        self.running = False

    # -----------------------
    # HALT SYSTEM (WATCHDOG)
    # -----------------------
    def halt(self):
        self.halted = True

    def resume(self):
        self.halted = False

    # -----------------------
    # STATUS
    # -----------------------
    def alive(self):
        return self.running