import os
import shutil
from pathlib import Path
import sys

# Configurable paths
BASE_DIR = Path("C:/Umbra")
GUI_DIR = BASE_DIR / "gui"
INITIAL_FILE_NAME = "first_script.py"

def create_directory(path: Path, dry_run: bool) -> None:
    """Create a directory if it doesn't exist."""
    try:
        if path.exists():
            print(f"Directory '{path}' already exists.")
        else:
            if not dry_run:
                path.mkdir(parents=True)
            print(f"Created directory '{path}'.")
    except Exception as e:
        print(f"Error creating directory '{path}': {e}")
        sys.exit(1)

def create_initial_file(file_path: Path, dry_run: bool) -> None:
    """Create an initial Python file."""
    try:
        if file_path.exists():
            print(f"File '{file_path}' already exists.")
        else:
            if not dry_run:
                with open(file_path, 'w') as f:
                    f.write("# This is the first script in the GUI directory.\n")
            print(f"Created initial Python file '{file_path}'.")
    except Exception as e:
        print(f"Error creating file '{file_path}': {e}")
        sys.exit(1)

def main(dry_run: bool) -> None:
    """Main function to create the directory and initial file."""
    print("Starting script execution.")
    
    # Create the GUI directory
    create_directory(GUI_DIR, dry_run)
    
    # Create the initial Python file
    initial_file_path = GUI_DIR / INITIAL_FILE_NAME
    create_initial_file(initial_file_path, dry_run)
    
    print("Script execution completed.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Create the first Python file in C:/Umbra/gui.")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry run without making changes to the filesystem.")
    
    args = parser.parse_args()
    
    main(args.dry_run)
