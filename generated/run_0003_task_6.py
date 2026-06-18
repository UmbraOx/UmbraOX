import os
import json
from urllib import request, error
from pathlib import Path

# Configuration constants
OLLAMA_URL = "http://localhost:11434"
WORLD_DOCUMENT_PATH = "world_document.txt"
DRY_RUN = False

def generate_content(prompt):
    try:
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'prompt': prompt})
        req = request.Request(OLLAMA_URL, data.encode('utf-8'), headers=headers)
        response = request.urlopen(req)
        return response.read().decode('utf-8')
    except error.URLError as e:
        print(f"Error connecting to Ollama: {e.reason}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def write_to_file(content, path):
    try:
        with open(path, 'a') as file:
            file.write(content)
        print(f"Content written to {path}")
    except IOError as e:
        print(f"Error writing to file {path}: {e.strerror}")

def main():
    prompt = "Generate content for the world document."
    if DRY_RUN:
        print("Dry run mode: skipping Ollama call and file write.")
    else:
        print("Connecting to Ollama...")
        content = generate_content(prompt)
        if content:
            print("Generating content...")
            write_to_file(content, WORLD_DOCUMENT_PATH)

if __name__ == '__main__':
    main()
