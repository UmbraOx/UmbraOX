import os
import http.server
import socketserver
from pathlib import Path
import shutil
import argparse
import subprocess

# Constants
DEFAULT_STATIC_DIR = 'static'
DEFAULT_PORT = 8000
LOG_FILE = 'server.log'

def create_static_directory(static_dir):
    """Create the static directory if it doesn't exist."""
    try:
        Path(static_dir).mkdir(parents=True, exist_ok=True)
        print(f"Static directory '{static_dir}' created successfully.")
    except FileExistsError:
        print(f"Static directory '{static_dir}' already exists.")
    except Exception as e:
        print(f"Failed to create static directory: {e}")
        raise

def serve_static_files(static_dir, port, dry_run):
    """Serve static files from the specified directory."""
    if dry_run:
        print("Dry run mode enabled. No changes will be made.")
        return

    handler = http.server.SimpleHTTPRequestHandler
    handler.directory = static_dir

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/)...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

def setup_logging():
    """Set up logging to a file."""
    try:
        with open(LOG_FILE, 'a') as log_file:
            pass  # Just create the file if it doesn't exist
        print(f"Logging enabled. Logs will be saved to {LOG_FILE}.")
    except Exception as e:
        print(f"Failed to set up logging: {e}")

def main():
    parser = argparse.ArgumentParser(description="Serve static files using a simple HTTP server.")
    parser.add_argument('--static-dir', default=DEFAULT_STATIC_DIR, help='Directory containing static files')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Port to serve on')
    parser.add_argument('--dry-run', action='store_true', help='Run the script without making changes')

    args = parser.parse_args()

    # Validate directory path
    if not Path(args.static_dir).is_absolute():
        print(f"Static directory path should be absolute. Using {Path.cwd() / args.static_dir}")
        args.static_dir = str(Path.cwd() / args.static_dir)

    # Create static directory
    create_static_directory(args.static_dir)

    # Set up logging
    setup_logging()

    # Serve static files
    serve_static_files(args.static_dir, args.port, args.dry_run)

if __name__ == "__main__":
    main()
