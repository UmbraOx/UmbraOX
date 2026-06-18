import os


class RuntimeFileAuditEngine:
    """
    Identifies safe-to-remove or redundant runtime files.
    """

    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.getcwd()

    def scan(self):
        candidates = []

        for root, _, files in os.walk(self.base_dir):
            for f in files:
                if not f.endswith(".py"):
                    continue

                path = os.path.join(root, f)

                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as file:
                        content = file.read()

                    score = self._score(content)

                    if score >= 3:
                        candidates.append({
                            "file": path,
                            "score": score,
                            "reason": self._reason(content)
                        })

                except Exception:
                    continue

        return sorted(candidates, key=lambda x: x["score"], reverse=True)

    def _score(self, content):
        score = 0
        if "TODO" in content:
            score += 1
        if "pass" in content:
            score += 2
        if len(content.splitlines()) < 20:
            score += 2
        if "NotImplemented" in content:
            score += 2
        return score

    def _reason(self, content):
        if len(content.splitlines()) < 20:
            return "Very small stub module"
        if "pass" in content:
            return "Contains placeholder logic"
        if "NotImplemented" in content:
            return "Unimplemented features"
        return "Low utility / candidate cleanup"

    def generate_report(self):
        return {
            "removable_candidates": self.scan(),
            "recommendation": "Review before deletion"
        }