from datetime import datetime
import os


class RuntimePatchController:
    """
    Governs ALL file modifications in Umbra.
    Nothing is allowed to mutate runtime without passing here.
    """

    def __init__(self, workspace_root=None):
        self.workspace_root = workspace_root or os.getcwd()
        self.approved_patches = []
        self.rejected_patches = []

    def approve_patch(self, file_path, diff, reason="manual approval"):
        patch = {
            "file": file_path,
            "diff": diff,
            "reason": reason,
            "approved_at": datetime.now().isoformat()
        }
        self.approved_patches.append(patch)
        return patch

    def reject_patch(self, file_path, diff, reason="not approved"):
        patch = {
            "file": file_path,
            "diff": diff,
            "reason": reason,
            "rejected_at": datetime.now().isoformat()
        }
        self.rejected_patches.append(patch)
        return patch

    def can_apply(self, file_path):
        return any(p["file"] == file_path for p in self.approved_patches)

    def require_approval(self, file_path):
        return not self.can_apply(file_path)

    def validate_patch_request(self, file_path, diff):
        """
        Central decision point for safety.
        """
        if not file_path:
            return False, "missing file_path"

        if ".." in file_path:
            return False, "path traversal blocked"

        return True, "ok"

    def summary(self):
        return {
            "approved": len(self.approved_patches),
            "rejected": len(self.rejected_patches)
        }