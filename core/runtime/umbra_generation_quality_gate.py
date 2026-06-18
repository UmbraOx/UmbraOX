class UmbraGenerationQualityGate:
    """
    Filters bad outputs BEFORE they reach UI or user.

    This is critical for:
    - image artifacts
    - broken sprites
    - incomplete game builds
    """

    def evaluate(self, asset: dict) -> dict:

        score = 1.0
        flags = []

        if asset.get("type") == "image":
            if asset.get("has_anatomy_errors"):
                score -= 0.5
                flags.append("anatomy_error")

        if asset.get("type") == "sprite":
            if asset.get("frame_inconsistency"):
                score -= 0.4
                flags.append("sprite_inconsistency")

        if asset.get("type") == "game":
            if not asset.get("playable_loop"):
                score -= 0.7
                flags.append("missing_game_loop")

        decision = "accept" if score >= 0.6 else "reject"

        return {
            "score": score,
            "flags": flags,
            "decision": decision
        }