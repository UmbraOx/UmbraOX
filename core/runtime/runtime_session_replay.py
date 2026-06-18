import json
import os
from datetime import datetime


class SessionReplay:

    def __init__(self, session_id, runs, metadata=None):
        self.session_id = session_id
        self.runs = runs
        self.metadata = metadata or {}
        self.replayed_at = datetime.now().isoformat()

    def to_dict(self):
        return {
            "session_id": self.session_id,
            "runs": self.runs,
            "metadata": self.metadata,
            "replayed_at": self.replayed_at,
            "total_runs": len(self.runs),
        }


class RuntimeSessionReplay:
    """
    Replay any past Umbra session.
    - Load session from disk
    - Re-execute prompts in order
    - Compare new results to original
    - Useful for regression testing and improvement validation
    """

    def __init__(self, sessions_dir=None, workspaces_dir=None):
        self.sessions_dir = sessions_dir or os.path.join(os.getcwd(), "sessions")
        self.workspaces_dir = workspaces_dir or os.path.join(os.getcwd(), "workspaces")
        self.replay_history = []

    def list_replayable_sessions(self):
        sessions = []
        if not os.path.exists(self.sessions_dir):
            return sessions
        for fname in os.listdir(self.sessions_dir):
            if fname.endswith(".json") and fname.startswith("session_"):
                path = os.path.join(self.sessions_dir, fname)
                try:
                    with open(path) as f:
                        data = json.load(f)
                    sessions.append({
                        "session_id": data.get("session_id", fname),
                        "run_count": len(data.get("runs", [])),
                        "created_at": data.get("created_at", ""),
                        "file": fname,
                    })
                except Exception:
                    pass
        return sorted(sessions, key=lambda s: s.get("created_at", ""), reverse=True)

    def load_session(self, session_id):
        path = os.path.join(self.sessions_dir, f"session_{session_id}.json")
        if not os.path.exists(path):
            for fname in os.listdir(self.sessions_dir):
                if session_id in fname and fname.endswith(".json"):
                    path = os.path.join(self.sessions_dir, fname)
                    break
            else:
                return None
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            return None

    def extract_prompts(self, session_data):
        prompts = []
        for run in session_data.get("runs", []):
            prompt = run.get("prompt", "")
            if prompt:
                prompts.append({
                    "prompt": prompt,
                    "original_run_id": run.get("run_id", ""),
                    "original_status": run.get("status", ""),
                    "original_files": len(run.get("written_files", [])),
                })
        return prompts

    def replay_session(self, session_id, pipeline, dry_run=False):
        session_data = self.load_session(session_id)
        if not session_data:
            return None

        prompts = self.extract_prompts(session_data)
        replay_runs = []

        for prompt_info in prompts:
            prompt = prompt_info["prompt"]
            if dry_run:
                replay_runs.append({
                    "prompt": prompt,
                    "original_run_id": prompt_info["original_run_id"],
                    "status": "dry_run_skipped",
                    "replayed": False,
                })
                continue

            run = pipeline.run(prompt)
            replay_runs.append({
                "prompt": prompt[:80],
                "original_run_id": prompt_info["original_run_id"],
                "original_status": prompt_info["original_status"],
                "original_files": prompt_info["original_files"],
                "new_run_id": run.run_id,
                "new_status": run.status,
                "new_files": len(run.written_files),
                "improved": len(run.written_files) >= prompt_info["original_files"],
                "replayed": True,
            })

        replay = SessionReplay(session_id, replay_runs, {
            "original_session": session_id,
            "dry_run": dry_run,
        })
        self.replay_history.append(replay.to_dict())
        return replay

    def compare_runs(self, original_run_id, new_run):
        original_path = os.path.join(self.workspaces_dir, original_run_id, "written_files.json")
        try:
            with open(original_path) as f:
                original_files = json.load(f)
        except Exception:
            original_files = []

        return {
            "original_file_count": len(original_files),
            "new_file_count": len(new_run.written_files),
            "improved": len(new_run.written_files) >= len(original_files),
            "new_status": new_run.status,
        }

    def get_replay_history(self):
        return list(self.replay_history)