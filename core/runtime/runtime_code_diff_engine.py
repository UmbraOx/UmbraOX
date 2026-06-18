import difflib


class RuntimeCodeDiffEngine:
    """
    Produces human-readable and machine-readable diffs
    for safe modification workflows.
    """

    def create_diff(self, old_code, new_code, filename="file.py"):
        diff = difflib.unified_diff(
            old_code.splitlines(keepends=True),
            new_code.splitlines(keepends=True),
            fromfile=f"{filename} (old)",
            tofile=f"{filename} (new)"
        )

        return "".join(diff)

    def summarize_changes(self, diff_text):
        added = sum(1 for line in diff_text.splitlines() if line.startswith("+") and not line.startswith("+++"))
        removed = sum(1 for line in diff_text.splitlines() if line.startswith("-") and not line.startswith("---"))

        return {
            "lines_added": added,
            "lines_removed": removed,
            "net_change": added - removed
        }