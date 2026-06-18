import urllib.request
import json

def fetch_game_design_document():
    """
    Fetches the full game design document from Ollama running at localhost:11434.
    
    Returns:
        str: The content of the game design document in markdown format.
        
    Raises:
        Exception: If there is an error fetching the document.
    """
    try:
        # URL to fetch the game design document
        url = "http://localhost:11434/game_design_document"
        
        # Send a GET request to the URL
        with urllib.request.urlopen(url) as response:
            # Read and decode the response
            response_data = response.read().decode('utf-8')
            
            # Parse the JSON response
            data = json.loads(response_data)
            
            # Extract the markdown content from the JSON data
            markdown_content = data.get('markdown', '')
            
            return markdown_content
    
    except urllib.error.URLError as e:
        raise Exception(f"Failed to fetch the game design document: {e.reason}")
    except json.JSONDecodeError:
        raise Exception("Failed to decode the response as JSON")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")

def save_markdown_to_file(markdown_content, filename="game_design_document.md"):
    """
    Saves the provided markdown content to a file.
    
    Args:
        markdown_content (str): The markdown content to be saved.
        filename (str): The name of the file to save the markdown content to.
        
    Raises:
        Exception: If there is an error writing the file.
    """
    try:
        # Open the file in write mode and write the markdown content
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(markdown_content)
    
    except IOError as e:
        raise Exception(f"Failed to save the markdown document: {e}")

def main():
    """
    Main function to fetch the game design document and save it as a markdown file.
    """
    try:
        # Fetch the game design document
        markdown_content = fetch_game_design_document()
        
        # Save the markdown content to a file
        save_markdown_to_file(markdown_content)
        
        print("Game design document saved successfully.")
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
