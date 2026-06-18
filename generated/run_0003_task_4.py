import json

class WorldDocument:
    def __init__(self):
        self.document = {
            "factions": {},
            "geography": {}
        }

    def tell_me_more(self, subject):
        """Provide more information about a given subject if available."""
        parts = subject.split()
        category = parts[0]
        name = ' '.join(parts[1:])
        
        if category in self.document and name in self.document[category]:
            return f"Information about {name}: {self.document[category][name]}"
        else:
            return f"No information available for {subject}."

    def add_faction(self, name, description):
        """Add a new faction to the world document."""
        if 'factions' not in self.document:
            self.document['factions'] = {}
        self.document['factions'][name] = description

    def add_geography(self, name, description):
        """Add a new geographical feature to the world document."""
        if 'geography' not in self.document:
            self.document['geography'] = {}
        self.document['geography'][name] = description

    def update_document(self, category, name, description):
        """Update or add an item in the specified category."""
        if category not in self.document:
            self.document[category] = {}
        self.document[category][name] = description

def main():
    world_doc = WorldDocument()
    
    while True:
        user_input = input("Ask a question or provide information (type 'exit' to quit): ").strip().lower()
        
        if user_input == 'exit':
            break
        elif user_input.startswith('tell me more about'):
            subject = user_input[len('tell me more about'):].strip()
            print(world_doc.tell_me_more(subject))
        elif user_input.startswith('add a'):
            parts = user_input.split(maxsplit=2)
            if len(parts) < 3:
                print("Invalid input format. Please use 'add a [category] [name] [description]'.")
                continue
            category, name, description = parts[1], parts[2], ' '.join(parts[3:])
            
            if category == 'faction':
                world_doc.add_faction(name, description)
            elif category == 'mountain range' or category == 'geography':
                world_doc.add_geography(name, description)
            else:
                print(f"Unsupported category: {category}. Please use 'faction' or 'mountain range'.")
        else:
            print("Invalid command. Please try again.")

if __name__ == "__main__":
    main()
