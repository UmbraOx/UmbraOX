from pathlib import Path


class RuntimeCodebaseIndexer:
    def index(self, root):
        results = []

        for path in Path(root).rglob("*.py"):
            results.append({
                "file": str(path),
                "name": path.name,
            })

        return results