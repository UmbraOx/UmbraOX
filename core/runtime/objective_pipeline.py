class ObjectivePipeline:

    def process(self, objective):

        lowered = objective.lower()

        domains = []

        keywords = {
            "ui": ["gui", "ui", "dashboard"],
            "agents": ["agent", "worker"],
            "runtime": ["runtime", "system"],
            "memory": ["memory", "persistent"],
            "deployment": ["deploy", "deployment"]
        }

        for domain, words in keywords.items():

            for word in words:

                if word in lowered:
                    domains.append(domain)
                    break

        if not domains:
            domains.append("runtime")

        return domains