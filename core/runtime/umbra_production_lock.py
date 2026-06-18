from core.runtime.umbra_activity_monitor import UmbraActivityMonitor
from core.runtime.umbra_resource_governor import UmbraResourceGovernor


class UmbraProductionLock:
    """
    FINAL HARD SAFETY LAYER

    Ensures:
    - Umbra does NOT interfere with user activity
    - Umbra throttles during gaming/streaming
    - Umbra runs safely during idle
    - Umbra cannot escalate compute usage
    """

    def __init__(self, spine, logger=None):
        self.spine = spine
        self.logger = logger

        self.monitor = UmbraActivityMonitor()
        self.governor = UmbraResourceGovernor()

    def tick(self):

        state = self.monitor.detect()

        if state == "user_active_heavy":
            self.governor.set_mode("gaming")

        elif state == "idle":
            self.governor.set_mode("idle")

        else:
            self.governor.set_mode("normal")

        policy = self.governor.apply_policy(self.spine)

        if self.logger:
            self.logger.log_event({
                "event": "production_lock_tick",
                "state": state,
                "policy": policy
            })

        return policy