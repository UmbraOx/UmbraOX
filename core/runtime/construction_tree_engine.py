class ConstructionTreeEngine:

    def construct(
        self,
        phases
    ):

        tree = {}

        previous = None

        for phase in phases:

            tree[phase] = []

            if previous:

                tree[previous].append(phase)

            previous = phase

        return tree