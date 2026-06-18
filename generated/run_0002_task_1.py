from typing import Dict, List

class CharacterSheet:
    """
    This class represents a character sheet for a game or story.
    It contains various attributes that define the character's characteristics.
    """

    def __init__(self, name: str, age: int, appearance: str, personality: str,
                 backstory: str, abilities: List[str], weaknesses: List[str],
                 relationships: Dict[str, str], voice_description: str, role: str):
        """
        Initializes a new instance of the CharacterSheet class.

        :param name: The character's name.
        :param age: The character's age.
        :param appearance: A description of the character's appearance.
        :param personality: A description of the character's personality traits.
        :param backstory: A brief overview of the character's background story.
        :param abilities: A list of the character's special abilities or skills.
        :param weaknesses: A list of the character's vulnerabilities or weaknesses.
        :param relationships: A dictionary describing the character's relationships with others.
        :param voice_description: A description of the character's voice.
        :param role: The character's role in the story or game.
        """
        self.name = name
        self.age = age
        self.appearance = appearance
        self.personality = personality
        self.backstory = backstory
        self.abilities = abilities
        self.weaknesses = weaknesses
        self.relationships = relationships
        self.voice_description = voice_description
        self.role = role

    def __str__(self) -> str:
        """
        Returns a string representation of the character sheet.

        :return: A formatted string containing all the character's attributes.
        """
        return (f"Character Sheet for {self.name}:\n"
                f"Age: {self.age}\n"
                f"Appearance: {self.appearance}\n"
                f"Personality: {self.personality}\n"
                f"Backstory: {self.backstory}\n"
                f"Abilities: {', '.join(self.abilities)}\n"
                f"Weaknesses: {', '.join(self.weaknesses)}\n"
                f"Relationships: {self.relationships}\n"
                f"Voice Description: {self.voice_description}\n"
                f"Role: {self.role}")

def create_character_sheet() -> CharacterSheet:
    """
    Creates a new character sheet with sample data.

    :return: An instance of the CharacterSheet class.
    """
    try:
        # Sample data for creating a character sheet
        name = "Aria Blackwood"
        age = 25
        appearance = "Tall and slender, with dark hair and piercing blue eyes."
        personality = "Determined and introverted, with a strong sense of justice."
        backstory = ("Aria lost her parents to a notorious criminal when she was young, "
                      "driving her to become a detective.")
        abilities = ["Expert investigator", "Master lock-picking"]
        weaknesses = ["Overconfidence in her skills", "Reluctance to ask for help"]
        relationships = {
            "best_friend": "Liam",
            "arch_enemy": "Dr. Malakai"
        }
        voice_description = "Rich and melodious, with a hint of mystery."
        role = "Lead detective"

        # Create an instance of CharacterSheet
        character_sheet = CharacterSheet(
            name=name,
            age=age,
            appearance=appearance,
            personality=personality,
            backstory=backstory,
            abilities=abilities,
            weaknesses=weaknesses,
            relationships=relationships,
            voice_description=voice_description,
            role=role
        )

        return character_sheet

    except Exception as e:
        print(f"An error occurred while creating the character sheet: {e}")
        raise

if __name__ == '__main__':
    # Create a character sheet and print it
    try:
        character = create_character_sheet()
        print(character)
    except Exception as e:
        print(f"Failed to run the script: {e}")
