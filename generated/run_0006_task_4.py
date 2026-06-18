import json
import os

class ConversationMemory:
    """
    A simple memory system to store conversations in JSON format.
    
    This class provides methods to add new conversations, load existing conversations,
    and save the current state of conversations to a file.
    """
    
    def __init__(self, filename='conversations.json'):
        """
        Initialize the ConversationMemory with a specified JSON file.
        
        :param filename: The name of the JSON file where conversations are stored.
        """
        self.filename = filename
        self.conversations = []
        
        # Load existing conversations if the file exists
        if os.path.exists(self.filename):
            self.load_conversations()
    
    def add_conversation(self, conversation):
        """
        Add a new conversation to the memory system.
        
        :param conversation: A dictionary representing the conversation.
        """
        if not isinstance(conversation, dict):
            raise ValueError("Conversation must be a dictionary.")
        
        self.conversations.append(conversation)
    
    def load_conversations(self):
        """
        Load conversations from the specified JSON file.
        """
        try:
            with open(self.filename, 'r') as file:
                self.conversations = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading conversations: {e}")
    
    def save_conversations(self):
        """
        Save the current conversations to the specified JSON file.
        """
        try:
            with open(self.filename, 'w') as file:
                json.dump(self.conversations, file, indent=4)
        except IOError as e:
            print(f"Error saving conversations: {e}")
    
    def get_conversations(self):
        """
        Return a list of all stored conversations.
        
        :return: A list of conversation dictionaries.
        """
        return self.conversations

# Example usage
if __name__ == "__main__":
    memory = ConversationMemory()
    
    # Add new conversations
    memory.add_conversation({"user": "Hello", "bot": "Hi there!"})
    memory.add_conversation({"user": "How are you?", "bot": "I'm just a computer program, but thanks for asking!"})
    
    # Save conversations to file
    memory.save_conversations()
    
    # Load conversations from file
    memory.load_conversations()
    
    # Print all conversations
    print(memory.get_conversations())
