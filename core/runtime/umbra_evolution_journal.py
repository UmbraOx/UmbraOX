import json
from pathlib import Path
from datetime import datetime


class UmbraEvolutionJournal:
    """
    Persistent memory for all self-modifications
    """

    def __init__(self, path="C:\\Umbra\\memory\\evolution_journal.json"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def log(self, entry: dict):
        data = json.loads(self.path.read_text(encoding="utf-8"))

        entry["timestamp"] = datetime.utcnow().isoformat()

        data.append(entry)

        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def history(self):
        return json.loads(self.path.read_text(encoding="utf-8"))