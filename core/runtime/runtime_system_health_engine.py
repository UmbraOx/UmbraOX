import os


class RuntimeSystemHealthEngine:
    """
    Produces a health score of the runtime system.
    Used for self-analysis and upgrade decisions.
    """

    def __init__(self, analyzer=None, dependency_engine=None):
        self.analyzer = analyzer
        self.dependency_engine = dependency_engine

    def evaluate(self, root="C:\\Umbra"):
        summary = self._analyze_basic(root)

        dependency_report = None
        if self.dependency_engine:
            dependency_report = self.dependency_engine.scan_directory(root)

        score = self._compute_score(summary, dependency_report)

        return {
            "summary": summary,
            "dependency": dependency_report,
            "health_score": score,
        }

    def _analyze_basic(self, root):
        total_files = 0
        total_lines = 0

        for dirpath, _, filenames in os.walk(root):
            for f in filenames:
                if f.endswith(".py"):
                    total_files += 1
                    try:
                        with open(os.path.join(dirpath, f), "r", encoding="utf-8") as fp:
                            total_lines += len(fp.readlines())
                    except Exception:
                        pass

        return {
            "total_files": total_files,
            "total_lines": total_lines,
        }

    def _compute_score(self, summary, dependency_report):
        base = 100

        if summary["total_files"] > 600:
            base -= 10

        if summary["total_lines"] > 500000:
            base -= 10

        if dependency_report and dependency_report.get("orphan_candidates"):
            base -= len(dependency_report["orphan_candidates"]) * 2

        return max(0, min(100, base))