import os
import sys
from pathlib import Path

# Configuration
DATA_DIR = Path("data")
CONFIG_FILE = DATA_DIR / "config.txt"
MOOD_FILE = DATA_DIR / "mood.txt"

# Constants
DRY_RUN = False  # Set to True for dry run mode

# Initialize mood
def initialize_mood():
    if not MOOD_FILE.exists():
        with open(MOOD_FILE, 'w') as f:
            f.write("neutral")
    return load_mood()

# Load mood from file
def load_mood():
    try:
        with open(MOOD_FILE, 'r') as f:
            mood = f.read().strip()
            print(f"Current mood: {mood}")
            return mood
    except IOError as e:
        print(f"Error loading mood: {e}")
        sys.exit(1)

# Save mood to file
def save_mood(mood):
    try:
        with open(MOOD_FILE, 'w') as f:
            f.write(mood)
            print(f"Mood saved: {mood}")
    except IOError as e:
        print(f"Error saving mood: {e}")
        sys.exit(1)

# Personality profile
def get_response(user_input, mood):
    responses = {
        "neutral": {
            "hello": "Hi there!",
            "how are you?": "I'm doing well, thanks for asking.",
            "bye": "Goodbye!"
        },
        "happy": {
            "hello": "Hello! What a wonderful day!",
            "how are you?": "Absolutely fantastic!",
            "bye": "Have a great day!"
        },
        "sad": {
            "hello": "Hi, it's not the best day for me.",
            "how are you?": "I'm feeling down today.",
            "bye": "Goodbye, take care."
        }
    }

    # Simple keyword matching
    for key in responses[mood]:
        if key in user_input.lower():
            return responses[mood][key]

    return "Sorry, I didn't understand that."

# Conversation loop
def conversation_loop():
    mood = initialize_mood()
    print("Starting conversation loop...")

    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("Exiting conversation.")
            break

        response = get_response(user_input, mood)
        print(f"Bot (Mood: {mood}): {response}")

        # Update mood based on user input
        if "happy" in user_input.lower():
            mood = "happy"
        elif "sad" in user_input.lower():
            mood = "sad"

        save_mood(mood)

if __name__ == "__main__":
    # Check for dry-run option
    if "--dry-run" in sys.argv:
        DRY_RUN = True
        print("Running in dry-run mode.")

    # Ensure data directory exists
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        print(f"Error creating data directory: {e}")
        sys.exit(1)

    conversation_loop()
