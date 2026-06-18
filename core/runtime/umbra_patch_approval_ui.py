import json
from pathlib import Path


class UmbraPatchApprovalUI:
    """
    Human-in-the-loop gate for all self-modification.
    Nothing gets applied without passing through here.
    """

    def __init__(self, approval_log_path="C:\\Umbra\\logs\\approvals.json"):
        self.log_path = Path(approval_log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def request_approval(self, proposal, diff: str) -> bool:
        print("\n=== PATCH PROPOSAL ===")
        print(proposal.file_path)
        print("\n--- DIFF ---\n")
        print(diff)

        decision = input("\nApprove patch? (y/n): ").strip().lower()

        self._log_decision(proposal.file_path, decision == "y")

        return decision == "y"

    def _log_decision(self, file_path, approved):
        record = {
            "file": file_path,
            "approved": approved
        }

        history = []
        if self.log_path.exists():
            history = json.loads(self.log_path.read_text())

        history.append(record)
        self.log_path.write_text(json.dumps(history, indent=2))