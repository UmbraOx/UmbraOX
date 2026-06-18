import os
from pathlib import Path
import shutil
import argparse

# Constants for paths (can be changed or passed as arguments)
SOURCE_DIR = Path('/path/to/source')
DEST_DIR = Path('/path/to/destination')

def copy_files(source, destination, dry_run=False):
    """
    Copy files from source directory to destination directory.
    
    :param source: Source directory path
    :param destination: Destination directory path
    :param dry_run: If True, perform a dry run without actually copying files
    """
    if not source.exists():
        print(f"Error: Source directory {source} does not exist.")
        return
    
    if not destination.exists():
        print(f"Creating destination directory {destination}")
        if not dry_run:
            destination.mkdir(parents=True)
    
    for item in source.iterdir():
        if item.is_file():
            dest_path = destination / item.name
            print(f"Copying {item} to {dest_path}")
            if not dry_run:
                shutil.copy2(item, dest_path)

def main():
    parser = argparse.ArgumentParser(description="Copy files from one directory to another.")
    parser.add_argument('--source', type=str, help='Source directory path')
    parser.add_argument('--destination', type=str, help='Destination directory path')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without copying files')

    args = parser.parse_args()

    source_path = Path(args.source) if args.source else SOURCE_DIR
    destination_path = Path(args.destination) if args.destination else DEST_DIR

    copy_files(source_path, destination_path, args.dry_run)

if __name__ == '__main__':
    main()
