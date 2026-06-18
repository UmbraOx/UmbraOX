import os
import json
from pathlib import Path

# Configurable paths
CHARACTER_SHEETS_DIR = 'character_sheets'

def generate_character_sheet(character_name, attributes=None, skills=None, inventory=None, is_dry_run=False):
    """
    Generates a character sheet as a JSON file based on user inputs.

    :param character_name: Name of the character
    :param attributes: Dictionary containing character attributes
    :param skills: List of character skills
    :param inventory: List of items in the character's inventory
    :param is_dry_run: If True, performs a dry run without saving the file
    """
    # Default values if not provided
    attributes = attributes or {}
    skills = skills or []
    inventory = inventory or []

    # Create the character sheet data structure
    character_sheet_data = {
        "character_name": character_name,
        "attributes": attributes,
        "skills": skills,
        "inventory": inventory
    }

    # Define the file path
    file_path = Path(CHARACTER_SHEETS_DIR) / f"{character_name}.json"

    # Ensure the directory exists
    if not is_dry_run:
        os.makedirs(file_path.parent, exist_ok=True)

    # Print progress
    print(f"Generating character sheet for {character_name}...")

    # Convert data to JSON and write to file (if not dry run)
    try:
        json_data = json.dumps(character_sheet_data, indent=4)
        if is_dry_run:
            print("Dry run: Character sheet would be saved with the following content:")
            print(json_data)
        else:
            with open(file_path, 'w') as file:
                file.write(json_data)
            print(f"Character sheet for {character_name} successfully generated and saved to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing the character sheet: {e}")

# Example usage
if __name__ == "__main__":
    # User inputs
    character_name = input("Enter the character's name: ")
    attributes_str = input("Enter character attributes (key:value pairs, separated by commas): ")
    skills_str = input("Enter character skills (comma-separated): ")
    inventory_str = input("Enter items in inventory (comma-separated): ")

    # Parse user inputs
    attributes = dict(item.split(':') for item in attributes_str.split(','))
    skills = [skill.strip() for skill in skills_str.split(',')]
    inventory = [item.strip() for item in inventory_str.split(',')]

    # Generate character sheet with dry run option
    is_dry_run_input = input("Perform a dry run? (yes/no): ").strip().lower()
    is_dry_run = is_dry_run_input == 'yes'

    generate_character_sheet(character_name, attributes, skills, inventory, is_dry_run)
