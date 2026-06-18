# core/runtime/improvement_proposal_engine.py


class ImprovementProposalEngine:

    def format(self, proposals):

        formatted = []

        for p in proposals:

            formatted.append({
                "id": p["id"],
                "title": p["goal"],
                "description": p["reason"],
                "target": p["file"],
                "type": p["type"]
            })

        print(f"[PROPOSAL_ENGINE] formatted {len(formatted)} proposals")

        return formatted