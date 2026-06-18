import re

def get_game_concept_description():
    """
    This function prompts the user to input a game concept description.
    It ensures that the description meets certain criteria (e.g., length) and returns it.
    
    Returns:
        str: A valid game concept description provided by the user.
    """
    while True:
        try:
            description = input("Please provide a game concept description (min 50 characters): ")
            
            # Check if the description meets the minimum length requirement
            if len(description) < 50:
                raise ValueError("The description must be at least 50 characters long.")
            
            # Optionally, you can add more validation logic here, such as checking for specific keywords or patterns
            if not re.search(r'\b(?:adventure|strategy|puzzle)\b', description, re.IGNORECASE):
                print("Note: Your description might benefit from including words like 'adventure', 'strategy', or 'puzzle'.")
            
            return description
        
        except ValueError as e:
            print(f"Invalid input: {e}. Please try again.")

if __name__ == '__main__':
    # Example usage of the function
    game_concept = get_game_concept_description()
    print("You entered the following game concept description:")
    print(game_concept)
