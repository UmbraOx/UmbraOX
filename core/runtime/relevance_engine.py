class RelevanceEngine:

    def filter(self, proposals):

        if not isinstance(
            proposals,
            list
        ):
            return []

        validated = []

        for proposal in proposals:

            if isinstance(
                proposal,
                dict
            ):

                validated.append(
                    proposal
                )

        return validated