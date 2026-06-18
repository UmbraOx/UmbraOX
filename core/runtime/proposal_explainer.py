class ProposalExplainer:

    def explain(self, proposal, prompt):

        title = proposal.get("title", "Unknown")
        target = proposal.get("target", "Unknown")
        proposal_type = proposal.get("type", "Unknown")

        return f"""
ARCHITECT EXPLANATION:

Umbra analyzed your request:

    "{prompt}"

PROPOSAL SUMMARY
----------------
Title:
{title}

Target:
{target}

Type:
{proposal_type}

ARCHITECT REASONING
-------------------
This proposal was generated because Umbra
identified a subsystem related to the
requested capability.

The target area would likely require:
- new runtime logic
- orchestration integration
- governance validation
- rollback protection
- execution isolation

Umbra is currently operating
in governance-only mode.

No automatic execution occurs.

If approved:
- detailed implementation plans
can be generated
- safe execution steps prepared
- dependency chains analyzed
- runtime integration validated

Current phase:
Architectural planning only.
"""