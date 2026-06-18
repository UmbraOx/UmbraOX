import os
import json


class FileIndex:

    def __init__(self):
        self.index_file = "memory/file_index.json"

    def build(self, workspace_data):

        os.makedirs("memory", exist_ok=True)

        with open(self.index_file, "w", encoding="utf-8") as f:
            json.dump(workspace_data, f, indent=4)

        print("[INDEX] File index updated")

    def load(self):

        if not os.path.exists(self.index_file):
            return []

        with open(self.index_file, "r", encoding="utf-8") as f:
            return json.load(f)