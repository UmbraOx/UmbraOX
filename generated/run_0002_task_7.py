import argparse
from character_design_ai import CharacterDesignAI  # Assuming this is your AI agent module

def main():
    """
    Main function to run the character design AI agent as a command-line application.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Character Design AI Agent")
    
    parser.add_argument(
        "--style",
        type=str,
        choices=["cartoon", "realistic", "fantasy"],
        default="cartoon",
        help="Style of the character design (default: cartoon)"
    )
    
    parser.add_argument(
        "--theme",
        type=str,
        required=True,
        help="Theme or concept for the character design"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="output.png",
        help="Output file path for the generated character design (default: output.png)"
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize the AI agent
        ai_agent = CharacterDesignAI(style=args.style)
        
        # Generate the character design
        ai_agent.generate_character(theme=args.theme, output_path=args.output)
        
        print(f"Character design generated and saved to {args.output}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
