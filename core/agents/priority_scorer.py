class PriorityScorer:
    """
    Ranks modules by upgrade importance
    """

    def score(self, modules: list) -> list:
        scored = []

        for m in modules:
            risk = 0

            # heuristics (expand later with LLM scoring)
            if m["function_count"] == 0:
                risk += 2

            if m["class_count"] == 0:
                risk += 1

            if len(m["imports"]) > 15:
                risk += 2

            scored.append({
                "file": m["file"],
                "reason": "auto_analysis",
                "priority": risk
            })

        return sorted(scored, key=lambda x: x["priority"], reverse=True)