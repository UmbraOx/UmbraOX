class CharacterSheet:
    def __init__(self):
        self.attributes = {
            "Strength": 10,
            "Dexterity": 10,
            "Constitution": 10,
            "Intelligence": 10,
            "Wisdom": 10,
            "Charisma": 10
        }
    
    def display_character_sheet(self):
        print("Character Sheet:")
        for attr, value in self.attributes.items():
            print(f"{attr}: {value}")
    
    def modify_attribute(self, attribute, change_value):
        if attribute not in self.attributes:
            raise ValueError(f"Attribute '{attribute}' not found.")
        
        try:
            change_value = int(change_value)
            new_value = self.attributes[attribute] + change_value
            if new_value < 0:
                print("Attribute value cannot be less than 0. Setting to 0 instead.")
                new_value = 0
            elif new_value > 20:
                print("Attribute value cannot exceed 20. Setting to 20 instead.")
                new_value = 20
            
            self.attributes[attribute] = new_value
            print(f"{attribute} updated to {new_value}.")
        except ValueError:
            raise ValueError(f"Invalid change value: '{change_value}'. Please enter an integer.")

def main():
    character_sheet = CharacterSheet()
    
    while True:
        character_sheet.display_character_sheet()
        
        user_input = input("Enter the attribute you want to modify and the change value (e.g., Strength +2, Dexterity -3): ")
        if user_input.lower() == "exit":
            print("Exiting program.")
            break
        
        parts = user_input.split()
        if len(parts) != 2:
            print("Invalid input format. Please use the format 'Attribute ChangeValue'.")
            continue
        
        attribute = parts[0]
        change_value = parts[1]
        
        try:
            character_sheet.modify_attribute(attribute, change_value)
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
