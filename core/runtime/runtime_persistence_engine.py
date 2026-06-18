import json


class RuntimePersistenceEngine:

    FILE = "runtime_state.json"

    def save(self, data):

        with open(self.FILE, "w") as f:
            json.dump(data, f, indent=2)

    def load(self):

        try:
            with open(self.FILE, "r") as f:
                return json.load(f)

        except:
            return {}