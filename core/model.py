import requests
import json
from core.config import OLLAMA_URL, MODEL_NAME


def ask_llm(prompt: str) -> str:
    """
    Safe LLM wrapper that guarantees string output.
    Prevents JSONDecodeError crashes from malformed responses.
    """

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        # Ollama returns: {"response": "..."}
        if "response" in data:
            return data["response"]

        return str(data)

    except Exception as e:
        return f'{{"error": "llm_failed", "message": "{str(e)}"}}'