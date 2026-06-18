from core.runtime.governance_state import GovernanceState

gov = GovernanceState()


def get_dashboard():

    return {
        "governance_mode": gov.mode,
        "approved": len(gov.approved),
        "rejected": len(gov.rejected),
        "status": "Umbra Control Center Active"
    }