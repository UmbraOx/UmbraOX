from core.runtime.proposal_batcher import ProposalBatcher
from core.runtime.proposal_explainer import ProposalExplainer
from core.runtime.governance_state import GovernanceState

from core.runtime.approval_execution_engine import (
    ApprovalExecutionEngine
)


class GovernanceEngine:

    def __init__(self, approval_store):

        self.approval_store = approval_store

        self.batcher = ProposalBatcher()

        self.explainer = ProposalExplainer()

        self.state = GovernanceState()

        self.execution_engine = (
            ApprovalExecutionEngine()
        )

    def build_batches(self, proposals, prompt):

        batches = self.batcher.batch(
            proposals
        )

        output = []

        for batch in batches:

            enriched = []

            for proposal in batch["proposals"]:

                explanation = self.explainer.explain(
                    proposal,
                    prompt
                )

                enriched.append({
                    "proposal": proposal,
                    "explanation": explanation,
                    "approved": False,
                })

            output.append({
                "batch_id": batch["id"],
                "items": enriched
            })

        return output

    def approve(self, proposal):

        proposal_id = proposal["id"]

        self.approval_store.approve(
            proposal_id
        )

        self.state.set_state(
            proposal_id,
            "approved"
        )

        preparation = (
            self.execution_engine.prepare(
                proposal
            )
        )

        return preparation

    def deny(self, proposal_id):

        self.approval_store.deny(
            proposal_id
        )

        self.state.set_state(
            proposal_id,
            "denied"
        )