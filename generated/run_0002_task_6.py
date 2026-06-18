import urllib.request
import urllib.parse
import json

class OllamaClient:
    """
    A client to interact with the Ollama AI model via HTTP.
    
    This class allows you to send requests to the Ollama API running on localhost:11434
    using the qwen2.5-coder:14b model.
    """
    
    def __init__(self, host: str = "localhost", port: int = 11434, model: str = "qwen2.5-coder:14b"):
        """
        Initialize the OllamaClient with the specified host, port, and model.
        
        :param host: The hostname where Ollama is running (default is 'localhost').
        :param port: The port number where Ollama is listening (default is 11434).
        :param model: The name of the AI model to use (default is 'qwen2.5-coder:14b').
        """
        self.base_url = f"http://{host}:{port}/api/v1/models/{model}/generate"
    
    def generate_text(self, prompt: str, max_tokens: int = 50) -> dict:
        """
        Generate text using the Ollama AI model.
        
        :param prompt: The input prompt for the AI model.
        :param max_tokens: The maximum number of tokens to generate (default is 50).
        :return: A dictionary containing the response from the API.
        :raises urllib.error.URLError: If there is a problem with the network request.
        :raises json.JSONDecodeError: If the response cannot be decoded as JSON.
        """
        data = {
            "prompt": prompt,
            "max_tokens": max_tokens
        }
        
        try:
            req = urllib.request.Request(
                self.base_url,
                method="POST",
                headers={"Content-Type": "application/json"},
                data=json.dumps(data).encode("utf-8")
            )
            with urllib.request.urlopen(req) as response:
                response_data = response.read().decode("utf-8")
                return json.loads(response_data)
        
        except urllib.error.URLError as e:
            raise RuntimeError(f"Failed to connect to Ollama API: {e.reason}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON response from the server: {str(e)}")

    def to_dict(self) -> dict:
        """
        Convert the client configuration to a dictionary.
        
        :return: A dictionary containing the host, port, and model information.
        """
        return {
            "host": self.base_url.split("//")[1].split(":")[0],
            "port": int(self.base_url.split(":")[-1]),
            "model": self.base_url.split("/")[-2]
        }

# Example usage:
if __name__ == "__main__":
    client = OllamaClient()
    
    try:
        response = client.generate_text("Hello, how can I assist you today?", max_tokens=50)
        print(response)
    except Exception as e:
        print(f"Error: {e}")
