import os
import shutil
from pathlib import Path
import argparse

# Constants for paths
SOURCE_DIR = Path(r'C:\Umbra\source')
DESTINATION_DIR = Path(r'C:\Umbra\destination')

def copy_files(source, destination, dry_run=False):
    """
    Copy files from the source directory to the destination directory.
    
    :param source: Source directory path
    :param destination: Destination directory path
    :param dry_run: If True, perform a dry run without actually copying files
    """
    try:
        if not os.path.exists(source):
            raise FileNotFoundError(f"Source directory '{source}' does not exist.")
        
        if not os.path.exists(destination):
            os.makedirs(destination)
            print(f"Created destination directory: {destination}")
        
        for index, file in enumerate(os.listdir(source)):
            src_file = Path(source) / file
            dest_file = Path(destination) / file
            
            if os.path.isfile(src_file):
                if dry_run:
                    print(f"Dry run - Would copy {src_file} to {dest_file}")
                else:
                    shutil.copy2(src_file, dest_file)
                    print(f"Copied {src_file} to {dest_file}")
        
        print("Copy operation completed successfully.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description="Copy files from source to destination directory.")
    parser.add_argument('--source', type=str, default=SOURCE_DIR, help='Source directory path')
    parser.add_argument('--destination', type=str, default=DESTINATION_DIR, help='Destination directory path')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without actually copying files')
    
    args = parser.parse_args()
    
    copy_files(args.source, args.destination, args.dry_run)

if __name__ == "__main__":
    main()
