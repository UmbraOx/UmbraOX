class RuntimeDecisionEngine:

    def score(
        self,
        option
    ):

        score = 0

        if option.get("safe"):
            score += 5

        if option.get("efficient"):
            score += 3

        if option.get("autonomous"):
            score += 2

        return score

    def choose(
        self,
        options
    ):

        ranked = sorted(
            options,
            key=self.score,
            reverse=True
        )

        return ranked[0] if ranked else None