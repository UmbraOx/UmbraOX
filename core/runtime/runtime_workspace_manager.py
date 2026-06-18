import os
import shutil
from datetime import datetime


class Workspace:
    def __init__(self, workspace_id, base_path):
        self.workspace_id = workspace_id
        self.base_path = base_path
        self.created_at = datetime.now().isoformat()
        self.log = []

    def write_file(self, relative_path, content):
        full = os.path.join(self.base_path, relative_path)
        os.makedirs(os.path.dirname(full), exist_ok=True)

        with open(full, "w", encoding="utf-8") as f:
            f.write(content)

        self.log.append({"action": "write", "path": relative_path})
        return full

    def list_files(self):
        out = []
        for root, _, files in os.walk(self.base_path):
            for f in files:
                out.append(os.path.relpath(os.path.join(root, f), self.base_path))
        return out

    def delete_file(self, relative_path):
        full = os.path.join(self.base_path, relative_path)
        if os.path.exists(full):
            os.remove(full)
            return True
        return False


class RuntimeWorkspaceManager:
    def __init__(self, base_dir=None):
        self.base_dir = base_dir or os.path.join(os.getcwd(), "workspaces")
        self.workspaces = {}
        os.makedirs(self.base_dir, exist_ok=True)

    def create_workspace(self, workspace_id):
        if workspace_id in self.workspaces:
            return self.workspaces[workspace_id]

        path = os.path.join(self.base_dir, workspace_id)
        os.makedirs(path, exist_ok=True)

        ws = Workspace(workspace_id, path)
        self.workspaces[workspace_id] = ws
        return ws

    def get_workspace(self, workspace_id):
        return self.workspaces.get(workspace_id)

    def destroy_workspace(self, workspace_id):
        ws = self.workspaces.get(workspace_id)
        if ws:
            shutil.rmtree(ws.base_path, ignore_errors=True)
        self.workspaces.pop(workspace_id, None)