from pathlib import Path


class RuntimeFilesystemScanner:
    def scan(self, root):
        root_path = Path(root)

        results = {
            "files": [],
            "directories": [],
        }

        for path in root_path.rglob("*"):
            if path.is_dir():
                results["directories"].append(str(path))
            else:
                results["files"].append(str(path))

        return results