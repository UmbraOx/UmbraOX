"""
RuntimeProjectManager — manages named projects across sessions.
Each project is isolated with its own folder, files, history, and status.
"""

import os
import json
from datetime import datetime


class UmbraProject:

    def __init__(self, name, project_type="general", description=""):
        self.name = name
        self.slug = name.lower().replace(" ", "_")
        self.project_type = project_type
        self.description = description
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"
        self.files = []
        self.conversation = []
        self.metadata = {}
        self.tags = []

    def to_dict(self):
        return {
            "name": self.name,
            "slug": self.slug,
            "project_type": self.project_type,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status,
            "files": self.files,
            "conversation": self.conversation[-20:],
            "metadata": self.metadata,
            "tags": self.tags,
        }

    @classmethod
    def from_dict(cls, data):
        p = cls(data["name"], data.get("project_type", "general"), data.get("description", ""))
        p.slug = data.get("slug", p.slug)
        p.created_at = data.get("created_at", p.created_at)
        p.updated_at = data.get("updated_at", p.updated_at)
        p.status = data.get("status", "active")
        p.files = data.get("files", [])
        p.conversation = data.get("conversation", [])
        p.metadata = data.get("metadata", {})
        p.tags = data.get("tags", [])
        return p


class RuntimeProjectManager:
    """
    Manages all Umbra projects across sessions.
    Projects are isolated — nothing overwrites another project.
    """

    def __init__(self, projects_dir):
        self.projects_dir = projects_dir
        os.makedirs(projects_dir, exist_ok=True)
        self._projects = {}
        self._active_project = None
        self._load_all()

    def _project_file(self, slug):
        return os.path.join(self.projects_dir, slug, "project.json")

    def _load_all(self):
        if not os.path.exists(self.projects_dir):
            return
        for entry in os.scandir(self.projects_dir):
            if entry.is_dir():
                pfile = os.path.join(entry.path, "project.json")
                if os.path.exists(pfile):
                    try:
                        with open(pfile, "r", encoding="utf-8") as f:
                            data = json.load(f)
                        p = UmbraProject.from_dict(data)
                        self._projects[p.slug] = p
                    except Exception:
                        pass

    def create_project(self, name, project_type="general", description=""):
        slug = name.lower().replace(" ", "_")
        if slug in self._projects:
            return self._projects[slug]

        project = UmbraProject(name, project_type, description)
        project_dir = os.path.join(self.projects_dir, slug)
        os.makedirs(os.path.join(project_dir, "code"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "assets"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "docs"), exist_ok=True)

        self._projects[slug] = project
        self.save_project(project)
        return project

    def get_project(self, name_or_slug):
        slug = name_or_slug.lower().replace(" ", "_")
        return self._projects.get(slug)

    def list_projects(self):
        return list(self._projects.values())

    def set_active(self, name_or_slug):
        slug = name_or_slug.lower().replace(" ", "_")
        if slug in self._projects:
            self._active_project = self._projects[slug]
            return self._active_project
        return None

    def get_active(self):
        return self._active_project

    def save_project(self, project):
        project.updated_at = datetime.now().isoformat()
        project_dir = os.path.join(self.projects_dir, project.slug)
        os.makedirs(project_dir, exist_ok=True)
        with open(self._project_file(project.slug), "w", encoding="utf-8") as f:
            json.dump(project.to_dict(), f, indent=2)

    def add_file_to_project(self, project, file_path, file_type="code"):
        entry = {
            "path": file_path,
            "type": file_type,
            "added_at": datetime.now().isoformat(),
        }
        project.files.append(entry)
        self.save_project(project)

    def add_conversation_turn(self, project, role, content):
        project.conversation.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        self.save_project(project)

    def get_project_dir(self, project):
        return os.path.join(self.projects_dir, project.slug)

    def get_project_summary(self, project):
        lines = [
            f"Project: {project.name}",
            f"Type: {project.project_type}",
            f"Files: {len(project.files)}",
            f"Status: {project.status}",
        ]
        if project.description:
            lines.append(f"Description: {project.description[:100]}")
        return "\n".join(lines)