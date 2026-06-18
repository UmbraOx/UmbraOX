class Decomposer:

    def split(self, task: str):
        """
        Converts a natural language task into structured subtasks.
        Phase 1: deterministic decomposition (no LLM required yet)
        """

        task = task.lower()

        # BASIC FILE OPERATIONS
        if "folder" in task:
            name = self._extract_name(task)
            return [
                {"goal": "create folder", "action": "create_folder", "path": name}
            ]

        if "file" in task:
            name = self._extract_name(task)
            content = self._extract_content(task)

            return [
                {
                    "goal": "create file",
                    "action": "create_file",
                    "path": name,
                    "content": content
                }
            ]

        # DEFAULT FALLBACK
        return [
            {"goal": "unknown task", "action": "log", "message": task}
        ]

    def _extract_name(self, task: str):
        # simple heuristic extraction
        words = task.split()
        for i, w in enumerate(words):
            if w in ["named", "called"]:
                if i + 1 < len(words):
                    return words[i + 1]
        return "unknown"

    def _extract_content(self, task: str):
        if "print" in task:
            start = task.find("print")
            return task[start:].strip()
        return ""