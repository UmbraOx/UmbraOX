class RuntimeExpansionManager:

    def expand(
        self,
        domains
    ):
        return [
            f"{domain}_expansion"
            for domain in domains
        ]