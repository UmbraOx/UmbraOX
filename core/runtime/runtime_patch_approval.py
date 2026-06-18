class RuntimePatchApproval:
    """
    Approval gate for self-modification.
    Prevents unsafe automatic overwrites.
    """

    def request_approval(self, file_path, diff):
        """
        In full system this would connect to GUI.
        For now: default SAFE = False (manual approval required).
        """

        return {
            "file": file_path,
            "approved": False,
            "reason": "manual_approval_required",
            "diff_preview": diff[:2000],
        }