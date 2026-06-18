import os
from datetime import datetime


class ProjectBlueprint:
    def __init__(self, name, project_type, description):
        self.name = name
        self.project_type = project_type
        self.description = description
        self.files = {}
        self.created_at = datetime.now().isoformat()

    def add_file(self, path, content):
        self.files[path] = content

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.project_type,
            "files": list(self.files.keys()),
            "created_at": self.created_at
        }


class RuntimeProjectBuilder:
    def __init__(self, writer=None):
        self.writer = writer
        self.history = []

    def build(self, name, project_type="script", description="", output_dir=None):
        bp = ProjectBlueprint(name, project_type, description)

        if project_type == "script":
            bp.add_file("main.py", f'print("{name} running")')

        elif project_type == "cli":
            bp.add_file("main.py", f"""
import argparse

def main():
    print("{name} CLI running")

if __name__ == "__main__":
    main()
""")

        elif project_type == "library":
            bp.add_file(f"{name}.py", f"class {name.title()}:\n    pass")

        # write files
        if output_dir:
            for path, content in bp.files.items():
                full = os.path.join(output_dir, path)
                os.makedirs(os.path.dirname(full), exist_ok=True)
                with open(full, "w", encoding="utf-8") as f:
                    f.write(content)

        self.history.append(bp.to_dict())
        return bp