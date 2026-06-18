import os
import shutil
from pathlib import Path

# Configuration
STATIC_DIR = Path("gui/static/")
VALID_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_")
DRY_RUN = False  # Set to True for dry run mode

def is_valid_filename(filename):
    """Check if the filename contains only valid characters."""
    return all(char in VALID_CHARS for char in filename)

def rename_file(src, dest):
    """Rename a file from src to dest with error handling."""
    try:
        if DRY_RUN:
            print(f"Dry Run: Would move {src} to {dest}")
        else:
            shutil.move(str(src), str(dest))
            print(f"Moved {src} to {dest}")
    except Exception as e:
        print(f"Error moving {src}: {e}")

def process_static_files():
    """Process static files in the directory."""
    if not STATIC_DIR.exists():
        print(f"The directory {STATIC_DIR} does not exist.")
        return

    for file_path in STATIC_DIR.iterdir():
        if file_path.is_file():
            filename = file_path.name
            base_name, ext = os.path.splitext(filename)
            
            # Check if the filename is valid
            if not is_valid_filename(base_name):
                new_base_name = ''.join(char if char in VALID_CHARS else '_' for char in base_name)
                new_filename = f"{new_base_name}{ext}"
                new_file_path = STATIC_DIR / new_filename
                
                print(f"Invalid filename detected: {filename}")
                rename_file(file_path, new_file_path)

if __name__ == "__main__":
    process_static_files()
