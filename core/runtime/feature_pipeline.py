from core.runtime.feature_synthesizer import FeatureSynthesizer
from core.runtime.self_improvement_loop import SelfImprovementLoop


class FeaturePipeline:
    """
    Converts prompt → stable feature objects
    Guarantees:
    - list output
    - no nested execution loops
    - no callable injection
    """

    def __init__(self):
        self.synth = FeatureSynthesizer()
        self.improvement = SelfImprovementLoop()

    def process(self, prompt: str):

        raw_features = self.synth.synthesize(prompt)

        # -----------------------------
        # NORMALIZE OUTPUT SAFETY
        # -----------------------------
        if raw_features is None:
            return []

        if isinstance(raw_features, dict):
            raw_features = [raw_features]

        if not isinstance(raw_features, list):
            raise TypeError(f"FeatureSynthesizer returned invalid type: {type(raw_features)}")

        enriched = []

        # -----------------------------
        # RUN IMPROVEMENT ONCE (NOT PER FEATURE)
        # -----------------------------
        proposals = self.improvement.run()

        # SAFETY: proposals must never be callable or dict-functions
        if callable(proposals):
            raise TypeError("SelfImprovementLoop returned callable (INVALID)")

        if isinstance(proposals, list) is False:
            proposals = [proposals]

        # -----------------------------
        # BUILD STABLE FEATURE STRUCTURES
        # -----------------------------
        for f in raw_features:

            if not isinstance(f, dict):
                f = {"value": f}

            enriched.append({
                **f,
                "proposals": proposals
            })

        return enriched