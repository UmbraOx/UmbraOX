import json
from pathlib import Path
from datetime import datetime


class UmbraEvolutionReplayLogger:
    """
    Full trace logging + replay capability for every evolution step.
    """

    def __init__(self, base_path="C:\\Umbra"):
        self.log_dir = Path(base_path) / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.session_file = self.log_dir / "evolution_session.json"
        self.session = []

    def log_event(self, event: dict):
        event["timestamp"] = datetime.utcnow().isoformat()
        self.session.append(event)
        self._flush()

    def _flush(self):
        self.session_file.write_text(json.dumps(self.session, indent=2))

    def load_session(self):
        if self.session_file.exists():
            return json.loads(self.session_file.read_text())
        return []

    def replay(self):
        for event in self.load_session():
            print(f"[REPLAY] {event}")