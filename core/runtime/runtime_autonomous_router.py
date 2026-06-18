class RuntimeAutonomousRouter:

    def route(self, domains):

        routes = {}

        for domain in domains:

            routes[domain] = f"core/{domain}"

        return routes