# core/runtime/approval_system.py


class ApprovalSystem:

    def approve(self, upgrade):

        print(
            f"[APPROVAL] approved: "
            f"{upgrade['id']}"
        )

        return True

    def reject(self, upgrade):

        print(
            f"[APPROVAL] rejected: "
            f"{upgrade['id']}"
        )

        return False