from core.runtime.intelligent_proposal_engine import (
    IntelligentProposalEngine
)

from core.runtime.relevance_engine import (
    RelevanceEngine
)

from core.runtime.feature_router import (
    FeatureRouter
)


class SelfImprovementLoop:

    def __init__(self):

        self.generator = (
            IntelligentProposalEngine()
        )

        self.relevance = (
            RelevanceEngine()
        )

        self.router = (
            FeatureRouter()
        )

    def generate(self, prompt):

        generated = (
            self.generator.generate(prompt)
        )

        proposals = (
            self.relevance.filter(
                generated
            )
        )

        routed = (
            self.router.route(
                proposals
            )
        )

        return routed