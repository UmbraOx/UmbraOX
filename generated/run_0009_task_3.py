import os
from pathlib import Path
import shutil
import subprocess

# Constants for paths (make them configurable)
PROJECT_ROOT = "web_server_project"
SUBDIRECTORIES = ["logs", "config", "static", "templates"]

def create_directory(path):
    try:
        path.mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {path}")
    except FileExistsError:
        print(f"Directory already exists: {path}")
    except PermissionError:
        print(f"Permission denied to create directory: {path}")

def main(dry_run=False):
    # Create the root project directory
    project_path = Path(PROJECT_ROOT)
    if dry_run:
        print(f"Dry-run: Would create project directory at {project_path}")
    else:
        create_directory(project_path)

    # Create subdirectories
    for subdir in SUBDIRECTORIES:
        subdir_path = project_path / subdir
        if dry_run:
            print(f"Dry-run: Would create subdirectory at {subdir_path}")
        else:
            create_directory(subdir_path)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create a new web server project directory.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without creating directories")
    
    args = parser.parse_args()
    
    main(dry_run=args.dry_run)
