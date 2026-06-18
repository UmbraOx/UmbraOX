import os
import json

def document_changes(file_path, changes):
    """
    Document changes made to a file.

    Args:
        file_path (str): The path to the file where changes will be documented.
        changes (list of str): A list of change descriptions.

    Returns:
        None
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    try:
        with open(file_path, 'r+') as file:
            content = json.load(file)
            if 'changes' in content:
                content['changes'].extend(changes)
            else:
                content['changes'] = changes
            file.seek(0)
            json.dump(content, file, indent=4)
            file.truncate()
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON from {file_path}: {e}")
    except Exception as e:
        print(f"An error occurred while documenting changes: {e}")

# Example usage
if __name__ == "__main__":
    # Assuming gui_server.py is a JSON file that stores documentation of changes
    file_path = 'gui_server.json'
    
    # List of changes to be documented
    changes = [
        "Added feature X to handle new data type Y.",
        "Modified function Z to improve performance by 20%."
    ]
    
    document_changes(file_path, changes)
