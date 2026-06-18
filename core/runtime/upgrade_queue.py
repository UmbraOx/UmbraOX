# core/runtime/upgrade_queue.py

import uuid


class UpgradeQueue:

    def __init__(self):

        self.pending = []

    # -------------------------------------------------
    # ADD
    # -------------------------------------------------

    def add_upgrade(self, filepath, content, reason):

        upgrade = {
            "id": str(uuid.uuid4())[:8],
            "filepath": filepath,
            "content": content,
            "reason": reason,
            "status": "pending"
        }

        self.pending.append(upgrade)

        print(f"[UPGRADE_QUEUE] queued: {upgrade['id']}")

        return upgrade

    # -------------------------------------------------
    # LIST
    # -------------------------------------------------

    def list_upgrades(self):

        return self.pending

    # -------------------------------------------------
    # GET
    # -------------------------------------------------

    def get_upgrade(self, upgrade_id):

        for item in self.pending:

            if item["id"] == upgrade_id:
                return item

        return None

    # -------------------------------------------------
    # REMOVE
    # -------------------------------------------------

    def remove_upgrade(self, upgrade_id):

        self.pending = [
            u for u in self.pending
            if u["id"] != upgrade_id
        ]