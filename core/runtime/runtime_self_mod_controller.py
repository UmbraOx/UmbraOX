from core.runtime.runtime_patch_engine import RuntimePatchEngine
from core.runtime.runtime_patch_approval import RuntimePatchApproval


class RuntimeSelfModController:
    """
    Central controller for Umbra self-modification.
    Coordinates:
    - rewrite
    - diff
    - approval
    - patch apply
    """

    def __init__(self):
        self.patch_engine = RuntimePatchEngine()
        self.approval = RuntimePatchApproval()
        self.pending_changes = []

    def propose_change(self, file_path, new_content):
        """
        Stage a change safely before applying.
        """

        # Load current
        with open(file_path, "r", encoding="utf-8") as f:
            original = f.read()

        diff = self.patch_engine.generate_diff(original, new_content, file_path)

        approval = self.approval.request_approval(file_path, diff)

        proposal = {
            "file": file_path,
            "diff": diff,
            "approved": approval["approved"],
        }

        self.pending_changes.append(proposal)

        return proposal

    def apply_change(self, file_path, new_content):
        """
        Apply after approval gate.
        """

        approval = self.approval.request_approval(file_path, "")

        if not approval["approved"]:
            return {
                "success": False,
                "reason": "not_approved",
            }

        result = self.patch_engine.apply_patch(file_path, new_content)
        return result.to_dict()

    def batch_apply(self, changes):
        results = []

        for change in changes:
            results.append(
                self.apply_change(
                    change["file"],
                    change["content"],
                )
            )

        return results

    def rollback(self, backup_path, target_path):
        return self.patch_engine.rollback(backup_path, target_path)