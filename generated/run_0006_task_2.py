def generate_emotional_response(situation):
    """
    Generate an emotional response based on the given situation.

    Parameters:
    situation (str): A description of the situation for which an emotional response is needed.

    Returns:
    str: An appropriate emotional response.
    """
    if not isinstance(situation, str):
        raise ValueError("The situation must be a string.")

    # Define a dictionary mapping situations to emotional responses
    responses = {
        "happy": "Yay! That's great!",
        "sad": "I'm sorry to hear that.",
        "angry": "It seems like you're feeling frustrated.",
        "excited": "Wow, that sounds thrilling!",
        "relaxed": "Sounds like a nice break from the usual routine.",
        "confused": "I don't quite understand. Can you explain more?",
        "default": "Hmm, I'm not sure how to respond to that."
    }

    # Normalize the situation input to lowercase
    situation = situation.lower()

    # Get the response based on the situation, default if not found
    return responses.get(situation, responses["default"])

# Example usage
if __name__ == "__main__":
    try:
        print(generate_emotional_response("Happy"))
        print(generate_emotional_response("sad"))
        print(generate_emotional_response("Angry"))
        print(generate_emotional_response("excited"))
        print(generate_emotional_response("relaxed"))
        print(generate_emotional_response("confused"))
        print(generate_emotional_response("unknown"))  # This will trigger the default response
    except ValueError as e:
        print(e)
