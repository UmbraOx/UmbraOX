import os
import pathlib
import shutil
import subprocess
import http.server
import socketserver

# Configuration options
STATIC_DIR = "gui/static"
PORT = 8000
DRY_RUN = False

def check_directory_exists(directory):
    """Check if the directory exists and is a directory."""
    path = pathlib.Path(directory)
    if not path.exists():
        print(f"Error: Directory '{directory}' does not exist.")
        return False
    if not path.is_dir():
        print(f"Error: '{directory}' is not a directory.")
        return False
    return True

def start_http_server(port, static_dir):
    """Start an HTTP server to serve files from the specified directory."""
    os.chdir(static_dir)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving HTTP on 0.0.0.0 port {port} (http://0.0.0.0:{port}/)...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nHTTP server stopped.")

def main():
    # Check if the static directory exists
    if not check_directory_exists(STATIC_DIR):
        return

    # Dry-run option
    if DRY_RUN:
        print(f"Dry run: Would start HTTP server on port {PORT} serving files from '{STATIC_DIR}'.")
        return

    # Start the HTTP server
    start_http_server(PORT, STATIC_DIR)

if __name__ == "__main__":
    main()
