# core/runtime/upgrade_executor.py

from core.runtime.self_upgrade_manager import (
    SelfUpgradeManager
)


class UpgradeExecutor:

    def __init__(self):

        self.manager = SelfUpgradeManager()

    # -------------------------------------------------
    # EXECUTE
    # -------------------------------------------------

    def execute(self, upgrade):

        result = self.manager.apply_upgrade(
            upgrade["filepath"],
            upgrade["content"]
        )

        print(
            f"[UPGRADE_EXECUTOR] applied: "
            f"{upgrade['id']}"
        )

        return result