import os
from pathlib import Path
import argparse
import sys

# Constants for default paths and options
DEFAULT_PROJECT_DIR = "new_project"
DRY_RUN = False

def navigate_to_directory(directory_path, dry_run=False):
    """
    Navigate to the specified directory.
    
    :param directory_path: Path to the directory to navigate to.
    :param dry_run: If True, simulate actions without actually changing directories.
    """
    try:
        # Check if the directory exists
        if not directory_path.exists():
            print(f"Directory '{directory_path}' does not exist.")
            return
        
        # Change the current working directory
        if not dry_run:
            os.chdir(directory_path)
            print(f"Navigated to '{directory_path}'.")
        else:
            print(f"Dry run: Would navigate to '{directory_path}'.")
    
    except Exception as e:
        print(f"An error occurred while navigating to '{directory_path}': {e}")
        sys.exit(1)

def main():
    # Setup argument parser
    parser = argparse.ArgumentParser(description="Navigate to a newly created project directory.")
    parser.add_argument('-p', '--project-dir', default=DEFAULT_PROJECT_DIR, help='Path to the new project directory.')
    parser.add_argument('--dry-run', action='store_true', help='Simulate actions without actually changing directories.')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Convert project directory to Path object
    project_dir_path = Path(args.project_dir)
    
    # Navigate to the specified directory
    navigate_to_directory(project_dir_path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
