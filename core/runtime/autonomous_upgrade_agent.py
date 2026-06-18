# core/runtime/autonomous_upgrade_agent.py

from core.runtime.upgrade_queue import UpgradeQueue


class AutonomousUpgradeAgent:

    def __init__(self):

        self.queue = UpgradeQueue()

    # -------------------------------------------------
    # PROPOSE
    # -------------------------------------------------

    def propose_upgrade(
        self,
        filepath,
        content,
        reason
    ):

        upgrade = self.queue.add_upgrade(
            filepath,
            content,
            reason
        )

        print(
            f"[UPGRADE_AGENT] proposal created: "
            f"{upgrade['id']}"
        )

        return upgrade

    # -------------------------------------------------
    # LIST
    # -------------------------------------------------

    def pending(self):

        return self.queue.list_upgrades()