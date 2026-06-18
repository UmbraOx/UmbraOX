import os


class RuntimeProjectIndexer:

    def index(self, root="."):

        indexed = []

        for path, dirs, files in os.walk(root):

            for file in files:

                indexed.append(
                    os.path.join(path, file)
                )

        return indexed