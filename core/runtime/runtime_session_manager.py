import json
import os
from datetime import datetime


class Session:

    def __init__(self, session_id, data=None):
        self.session_id = session_id
        self.data = data or {}
        self.created_at = data.get("created_at") if data else datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            **self.data,
        }


class RuntimeSessionManager:
    """
    Persistent cross-session state.
    Umbra remembers objectives, run history, and context between restarts.
    Saves to JSON files in sessions/ directory.
    """

    def __init__(self, sessions_dir=None):
        self.sessions_dir = sessions_dir or os.path.join(os.getcwd(), "sessions")
        os.makedirs(self.sessions_dir, exist_ok=True)
        self.active_sessions = {}

    def create_session(self, session_id=None):
        if session_id is None:
            session_id = datetime.now().strftime("session_%Y%m%d_%H%M%S")
        session = Session(session_id)
        self.active_sessions[session_id] = session
        return session

    def load_session(self, session_id):
        path = self._path(session_id)
        if not os.path.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        session = Session(session_id, data)
        self.active_sessions[session_id] = session
        return session

    def save_session(self, session_id):
        session = self.active_sessions.get(session_id)
        if not session:
            return False
        with open(self._path(session_id), "w", encoding="utf-8") as f:
            json.dump(session.to_dict(), f, indent=2)
        return True

    def save_all(self):
        for session_id in self.active_sessions:
            self.save_session(session_id)

    def get_session(self, session_id):
        return self.active_sessions.get(session_id)

    def load_or_create(self, session_id):
        existing = self.load_session(session_id)
        if existing:
            return existing
        return self.create_session(session_id)

    def list_saved_sessions(self):
        files = [f for f in os.listdir(self.sessions_dir) if f.endswith(".json")]
        return [f.replace(".json", "") for f in sorted(files)]

    def delete_session(self, session_id):
        self.active_sessions.pop(session_id, None)
        path = self._path(session_id)
        if os.path.exists(path):
            os.remove(path)
            return True
        return False

    def get_latest_session_id(self):
        saved = self.list_saved_sessions()
        return saved[-1] if saved else None

    def record_run(self, session_id, run_dict):
        session = self.active_sessions.get(session_id)
        if not session:
            return
        runs = session.get("run_history", [])
        runs.append({
            "run_id": run_dict.get("run_id"),
            "status": run_dict.get("status"),
            "prompt": run_dict.get("prompt", "")[:100],
            "recorded_at": datetime.now().isoformat(),
        })
        session.set("run_history", runs[-50:])  # keep last 50
        self.save_session(session_id)

    def get_run_history(self, session_id):
        session = self.load_session(session_id)
        if not session:
            return []
        return session.get("run_history", [])

    def _path(self, session_id):
        safe_id = session_id.replace("/", "_").replace("\\", "_")
        return os.path.join(self.sessions_dir, f"{safe_id}.json")