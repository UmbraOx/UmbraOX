import os
from pathlib import Path
from typing import Union

# Constants for file paths (can be overridden by function arguments)
CONVERSATION_HISTORY_PATH = "conversation_history.txt"
PERSONALITY_PROFILE_PATH = "personality_profile.json"

def save_to_file(file_path: Union[str, Path], data: str, dry_run: bool = False) -> None:
    """
    Save the given data to a file at the specified path.
    
    :param file_path: The path where the file should be saved.
    :param data: The data to write to the file.
    :param dry_run: If True, perform a dry run without actually writing to the file.
    """
    if dry_run:
        print(f"Dry-run: Would save data to {file_path}")
    else:
        try:
            with open(file_path, 'w') as file:
                file.write(data)
            print(f"Data saved successfully to {file_path}")
        except IOError as e:
            print(f"An error occurred while saving data to {file_path}: {e}")

def save_conversation_history(history_data: str, history_path: Union[str, Path] = CONVERSATION_HISTORY_PATH, dry_run: bool = False) -> None:
    """
    Save conversation history to a file.
    
    :param history_data: The conversation history data as a string.
    :param history_path: The path where the conversation history should be saved. Defaults to CONVERSATION_HISTORY_PATH.
    :param dry_run: If True, perform a dry run without actually writing to the file.
    """
    print("Saving conversation history...")
    save_to_file(history_path, history_data, dry_run)

def save_personality_profile(profile_data: str, profile_path: Union[str, Path] = PERSONALITY_PROFILE_PATH, dry_run: bool = False) -> None:
    """
    Save personality profile to a file.
    
    :param profile_data: The personality profile data as a string.
    :param profile_path: The path where the personality profile should be saved. Defaults to PERSONALITY_PROFILE_PATH.
    :param dry_run: If True, perform a dry run without actually writing to the file.
    """
    print("Saving personality profile...")
    save_to_file(profile_path, profile_data, dry_run)

# Example usage:
if __name__ == "__main__":
    conversation_history = "Example conversation history data"
    personality_profile = '{"trait1": "value1", "trait2": "value2"}'
    
    # Save with default paths and without dry-run
    save_conversation_history(conversation_history)
    save_personality_profile(personality_profile)
    
    # Save with custom paths and perform a dry-run
    save_conversation_history(conversation_history, history_path="custom_history.txt", dry_run=True)
    save_personality_profile(personality_profile, profile_path="custom_profile.json", dry_run=True)
