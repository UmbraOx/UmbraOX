import time
import threading


class UmbraUnifiedRuntime:
    """
    FINAL SYSTEM ORCHESTRATOR

    THIS IS THE REAL "START UMBRA" ENTRY CORE.

    Responsibilities:
    - run kernel
    - trigger boss agent cycles
    - initiate upgrade pipeline
    - enforce watchdog safety
    """

    def __init__(self, kernel, boss_agent, upgrade_engine, watchdog, interval=5):
        self.kernel = kernel
        self.boss_agent = boss_agent
        self.upgrade_engine = upgrade_engine
        self.watchdog = watchdog

        self.interval = interval
        self.running = False

        self.last_cycle = time.time()

    # ----------------------------
    # SYSTEM CYCLE
    # ----------------------------
    def cycle(self):
        """
        ONE FULL EVOLUTION LOOP:
        1. audit system
        2. queue improvements
        3. execute next task
        4. optionally upgrade system
        """

        # 1. BossAgent audit phase
        audit_result = self.boss_agent.run_cycle()

        # 2. Execute next queued improvement
        execution_result = self.boss_agent.execute_next()

        # 3. If upgrade candidate exists, trigger pipeline
        upgrade_result = None

        if execution_result.get("diff") or execution_result.get("proposal"):

            proposal = execution_result

            try:
                self.upgrade_engine.stage_upgrade(proposal["proposal"])
                upgrade_result = self.upgrade_engine.apply(
                    backup_dir="C:\\Umbra\\backups"
                )
            except Exception as e:
                upgrade_result = {"status": "failed", "error": str(e)}

        return {
            "audit": audit_result,
            "execution": execution_result,
            "upgrade": upgrade_result
        }

    # ----------------------------
    # LOOP
    # ----------------------------
    def start(self):

        if self.running:
            return

        self.running = True
        self.kernel.start()

        def loop():
            while self.running:

                # watchdog gate (system health control)
                if self.watchdog and hasattr(self.watchdog, "healthy"):
                    if not self.watchdog.healthy():
                        time.sleep(1)
                        continue

                self.last_cycle = time.time()

                try:
                    self.cycle()
                except Exception:
                    pass

                time.sleep(self.interval)

        threading.Thread(target=loop, daemon=True).start()

    # ----------------------------
    # STOP
    # ----------------------------
    def stop(self):
        self.running = False
        self.kernel.stop()