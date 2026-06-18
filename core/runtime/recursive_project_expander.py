class RecursiveProjectExpander:

    def expand(self, domains):

        expansions = []

        for domain in domains:

            expansions.append(
                f"{domain}_expansion"
            )

        return expansions