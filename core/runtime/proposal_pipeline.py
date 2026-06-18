class ProposalPipeline:

    def generate(self, domains):

        proposals = []

        for domain in domains:

            proposals.append({
                "title": f"{domain.title()} System",
                "type": domain,
                "target": f"core/{domain}"
            })

        return proposals