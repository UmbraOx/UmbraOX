class ProjectGraphEngine:

    def build(self, domains):

        graph = {}

        previous = None

        for domain in domains:

            if previous:
                graph[domain] = [previous]
            else:
                graph[domain] = []

            previous = domain

        return graph