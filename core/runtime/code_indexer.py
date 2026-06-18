import os


class CodeIndexer:

    def __init__(self, root="."):
        self.root = root

    def index(self):

        indexed = []

        for root, dirs, files in os.walk(self.root):

            for file in files:

                if file.endswith(".py"):

                    path = os.path.join(root, file)

                    indexed.append(path)

        print(f"[INDEXER] indexed {len(indexed)} files")

        return {
            "files": indexed
        }