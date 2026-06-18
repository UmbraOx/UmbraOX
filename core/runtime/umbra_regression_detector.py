import difflib


class UmbraRegressionDetector:
    """
    Detects dangerous behavioral drift between versions.
    """

    def score_regression(self, before: str, after: str) -> float:
        diff = list(difflib.unified_diff(
            before.splitlines(),
            after.splitlines()
        ))

        # simple heuristic: large diff = higher risk
        change_ratio = len(diff) / max(1, len(before.splitlines()))

        return min(change_ratio, 1.0)

    def is_safe(self, score: float) -> bool:
        return score < 0.35