class ObjectiveInterpreter:

    def interpret(self, prompt: str):
        prompt = prompt.lower()

        domains = []

        mapping = {
            "ui": ["gui", "ui", "dashboard", "window", "desktop"],
            "agents": ["agent", "assistant", "worker", "multi agent"],
            "runtime": ["runtime", "system", "kernel", "autonomous"],
            "planning": ["plan", "planner", "objective", "goal"],
            "deployment": ["deploy", "deployment", "release", "installer"],
            "voice": ["voice", "speech", "audio", "microphone"],
            "memory": ["memory", "persistent", "storage"],
        }

        for domain, keywords in mapping.items():
            for keyword in keywords:
                if keyword in prompt:
                    domains.append(domain)
                    break

        if not domains:
            domains.append("runtime")

        return {
            "prompt": prompt,
            "domains": domains,
            "complexity": len(domains),
        }