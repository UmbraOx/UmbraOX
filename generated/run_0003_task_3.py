import os
from pathlib import Path
import json
import shutil
import subprocess

# Constants for paths
DEFAULT_MARKDOWN_PATH = "world_document.md"
DEFAULT_JSON_PATH = "world_document.json"

def save_world_document_as_markdown_and_json(markdown_content, json_data,
                                             markdown_path=DEFAULT_MARKDOWN_PATH,
                                             json_path=DEFAULT_JSON_PATH,
                                             dry_run=False):
    """
    Save the generated world document as both a markdown file and a JSON file.

    :param markdown_content: The content to be saved in the markdown file.
    :param json_data: The data to be saved in the JSON file.
    :param markdown_path: Path where the markdown file will be saved.
    :param json_path: Path where the JSON file will be saved.
    :param dry_run: If True, perform a dry run without actually writing files.
    """
    # Handle paths
    markdown_file = Path(markdown_path)
    json_file = Path(json_path)

    try:
        # Save as Markdown
        if not dry_run:
            with open(markdown_file, 'w', encoding='utf-8') as md_file:
                md_file.write(markdown_content)
        print(f"Saved markdown content to {markdown_path}")

        # Save as JSON
        if not dry_run:
            with open(json_file, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        print(f"Saved JSON data to {json_path}")

    except IOError as e:
        print(f"Error occurred while writing files: {e}")
        return False

    return True

# Example usage
if __name__ == "__main__":
    markdown_content = "# Sample Markdown\nThis is a sample markdown content."
    json_data = {
        "title": "Sample Document",
        "content": "This is a sample JSON data.",
        "items": [1, 2, 3]
    }

    # Perform a dry run
    print("Performing dry run...")
    save_world_document_as_markdown_and_json(markdown_content, json_data, dry_run=True)

    # Save files
    print("\nSaving files...")
    save_world_document_as_markdown_and_json(markdown_content, json_data)
