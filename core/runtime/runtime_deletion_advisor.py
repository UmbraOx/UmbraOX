class RuntimeDeletionAdvisor:
    """
    SAFE advisory system only.
    DOES NOT delete files.
    Only recommends candidates based on dependency scan.
    """

    def __init__(self, dependency_engine):
        self.dependency_engine = dependency_engine

    def recommend_deletions(self, root):
        report = self.dependency_engine.scan_directory(root)

        candidates = report.get("orphan_candidates", [])

        return {
            "safe_to_review": candidates,
            "warning": "These are NOT auto-delete. Human approval required.",
        }