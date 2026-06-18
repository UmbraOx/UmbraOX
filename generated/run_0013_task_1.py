import os
import subprocess
import argparse
from pathlib import Path

# Constants for paths
NGINX_CONF_PATH = "/etc/nginx/nginx.conf"
APACHE_CONF_PATH = "/etc/apache2/apache2.conf"
NODEJS_PROCESS_NAME = "node"

def check_file_exists(file_path):
    """Check if a file exists and is readable."""
    return Path(file_path).is_file()

def read_file(file_path):
    """Read the content of a file."""
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading {file_path}: {e}")
        return None

def check_process_running(process_name):
    """Check if a process is running."""
    try:
        result = subprocess.run(['pgrep', '-f', process_name], capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error checking for process {process_name}: {e}")
        return False

def identify_web_server():
    """Identify the web server or framework being used."""
    if check_file_exists(NGINX_CONF_PATH):
        nginx_content = read_file(NGINX_CONF_PATH)
        if nginx_content and "nginx" in nginx_content:
            print("Nginx is configured for static file serving.")
    
    if check_file_exists(APACHE_CONF_PATH):
        apache_content = read_file(APACHE_CONF_PATH)
        if apache_content and "apache2" in apache_content:
            print("Apache is configured for static file serving.")
    
    if check_process_running(NODEJS_PROCESS_NAME):
        print("Node.js process is running, which might be serving static files.")

def main():
    parser = argparse.ArgumentParser(description="Identify the web server or framework being used for static file serving.")
    args = parser.parse_args()

    identify_web_server()

if __name__ == "__main__":
    main()
