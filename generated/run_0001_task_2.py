from typing import Any, Dict

def determine_context(question: str) -> str:
    """
    Determine the context in which the question is asked.
    
    Parameters:
    - question (str): The question to analyze.
    
    Returns:
    - str: The determined context ('personal' or 'professional').
    """
    # Define keywords for personal and professional contexts
    personal_keywords = ["family", "health", "hobbies", "interests"]
    professional_keywords = ["work", "career", "job", "company", "project"]

    # Convert the question to lowercase for case-insensitive comparison
    lower_question = question.lower()

    # Check for personal keywords
    if any(keyword in lower_question for keyword in personal_keywords):
        return "personal"

    # Check for professional keywords
    if any(keyword in lower_question for keyword in professional_keywords):
        return "professional"

    # Default to personal if no clear context is found
    return "personal"

# Example usage
if __name__ == "__main__":
    try:
        question = input("Please enter your question: ")
        context = determine_context(question)
        print(f"The context of the question is: {context}")
    except Exception as e:
        print(f"An error occurred: {e}")
