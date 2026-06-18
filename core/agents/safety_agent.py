class SafetyAgent:

    def filter(self, proposals):

        safe = []

        for p in proposals:

            # NEVER allow system-level file modification without review
            if "__init__" in p.file_path:
                continue

            if len(p.diff) > 50000:
                continue

            safe.append(p)

        return safe