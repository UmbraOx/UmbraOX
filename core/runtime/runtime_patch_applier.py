class RuntimePatchApplier:
    def apply_patch(self, content, patch):
        return content.replace(
            patch["old"],
            patch["new"],
        )