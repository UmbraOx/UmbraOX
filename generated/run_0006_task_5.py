import random

class MoodSystem:
    """
    A simple mood system that changes based on the conversation context.
    
    The system has three moods: positive, neutral, and negative.
    It analyzes the input text to determine which mood to adopt.
    """

    def __init__(self):
        self.moods = ['positive', 'neutral', 'negative']
        self.current_mood = random.choice(self.moods)

    def analyze_text(self, text):
        """
        Analyzes the input text and returns a mood suggestion.
        
        :param text: The input text to analyze.
        :return: A suggested mood based on the text content.
        """
        keywords_positive = ['good', 'happy', 'great', 'excellent']
        keywords_negative = ['bad', 'sad', 'terrible', 'horrible']

        words = text.lower().split()
        
        if any(keyword in words for keyword in keywords_positive):
            return 'positive'
        elif any(keyword in words for keyword in keywords_negative):
            return 'negative'
        else:
            return 'neutral'

    def update_mood(self, text):
        """
        Updates the current mood based on the analyzed input text.
        
        :param text: The input text to analyze and use for updating the mood.
        """
        suggested_mood = self.analyze_text(text)
        if suggested_mood != self.current_mood:
            print(f"Mood changed from {self.current_mood} to {suggested_mood}")
        else:
            print(f"No change in mood: still {self.current_mood}")

        self.current_mood = suggested_mood

    def get_current_mood(self):
        """
        Returns the current mood of the system.
        
        :return: The current mood as a string.
        """
        return self.current_mood


# Example usage
if __name__ == "__main__":
    mood_system = MoodSystem()
    print(f"Initial mood: {mood_system.get_current_mood()}")

    conversation = [
        "I had a great day today!",
        "The weather is terrible.",
        "It's just an average day.",
        "I'm so happy to be here!"
    ]

    for text in conversation:
        print(f"\nInput: {text}")
        mood_system.update_mood(text)
        print(f"Current Mood: {mood_system.get_current_mood()}")
