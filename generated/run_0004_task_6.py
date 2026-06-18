import os
import shutil
from pathlib import Path
import subprocess
import argparse

# Constants for paths, modify these or pass them as arguments
SOURCE_DIR = Path('/path/to/source')
DEST_DIR = Path('/path/to/destination')

def copy_files(source: Path, dest: Path, dry_run: bool):
    """Copy files from source to destination directory."""
    try:
        if not os.path.exists(dest):
            os.makedirs(dest)
        
        for item in source.iterdir():
            s = source / item
            d = dest / item
            
            if s.is_dir():
                print(f"Copying directory {s} to {d}")
                if not dry_run:
                    shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                print(f"Copying file {s} to {d}")
                if not dry_run:
                    shutil.copy2(s, d)
    except Exception as e:
        print(f"Error copying files: {e}")

def run_command(command: str, dry_run: bool):
    """Run a shell command."""
    try:
        print(f"Running command: {command}")
        if not dry_run:
            subprocess.run(command, check=True, shell=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Automate tasks using Python.")
    parser.add_argument('--dry-run', action='store_true', help='Run the script without making actual changes.')
    args = parser.parse_args()

    dry_run = args.dry_run

    print("Starting automation script...")
    
    # Example task: Copy files
    copy_files(SOURCE_DIR, DEST_DIR, dry_run)
    
    # Example task: Run a command
    run_command('echo "Hello, World!"', dry_run)

    print("Automation script completed.")

if __name__ == '__main__':
    main()
