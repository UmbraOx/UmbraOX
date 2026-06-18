import os


class WorkspaceScanner:

    def scan(self, root="sandbox"):

        collected = []

        for current_root, dirs, files in os.walk(root):

            for d in dirs:
                collected.append({
                    "type": "folder",
                    "path": os.path.join(current_root, d)
                })

            for f in files:
                collected.append({
                    "type": "file",
                    "path": os.path.join(current_root, f)
                })

        return collected