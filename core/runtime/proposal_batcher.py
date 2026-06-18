import uuid


class ProposalBatcher:

    def batch(self, proposals, size=3):

        batches = []

        current = []

        for proposal in proposals:

            current.append(proposal)

            if len(current) >= size:

                batches.append({
                    "id": str(uuid.uuid4())[:8],
                    "proposals": current
                })

                current = []

        if current:

            batches.append({
                "id": str(uuid.uuid4())[:8],
                "proposals": current
            })

        return batches