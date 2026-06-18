class FeatureRouter:

    def route(self, proposals):

        if not isinstance(
            proposals,
            list
        ):
            proposals = []

        domains = []

        for proposal in proposals:

            target = proposal.get(
                "target",
                ""
            )

            if "ui" in target:
                domains.append("ui")

            if "agent" in target:
                domains.append("agents")

            if "runtime" in target:
                domains.append("runtime")

            if "deployment" in target:
                domains.append("deployment")

            if "memory" in target:
                domains.append("memory")

        return {
            "proposals": proposals,
            "domains": list(set(domains))
        }