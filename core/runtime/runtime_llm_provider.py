import json
import os
import urllib.request


class LLMResponse:
    def __init__(self, content, model, provider, tokens_used=0):
        self.content = content
        self.model = model
        self.provider = provider
        self.tokens_used = tokens_used
        self.success = True
        self.error = None

    @classmethod
    def error_response(cls, error, provider="unknown"):
        r = cls("", "", provider)
        r.success = False
        r.error = str(error)
        return r


class RuntimeLLMProvider:
    """
    Stable multi-provider LLM wrapper (Ollama-first safe mode).
    """

    PROVIDER_OLLAMA = "ollama"
    PROVIDER_OPENAI = "openai"
    PROVIDER_ANTHROPIC = "anthropic"
    PROVIDER_GROQ = "groq"

    DEFAULT_MODELS = {
        "ollama": "llama3",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-haiku-20241022",
        "groq": "llama3-8b-8192",
    }

    def __init__(self, provider=None, model=None, api_key=None):
        self.provider = provider or os.getenv("UMBRA_LLM_PROVIDER", self.PROVIDER_OLLAMA)
        self.model = model or self.DEFAULT_MODELS.get(self.provider, "llama3")
        self.api_key = api_key or os.getenv("UMBRA_LLM_API_KEY", "")
        self.base_url = self._base_url()

    def _base_url(self):
        return {
            self.PROVIDER_OLLAMA: "http://localhost:11434/api",
            self.PROVIDER_OPENAI: "https://api.openai.com/v1",
            self.PROVIDER_GROQ: "https://api.groq.com/openai/v1",
            self.PROVIDER_ANTHROPIC: "https://api.anthropic.com/v1",
        }.get(self.provider, "http://localhost:11434/api")

    def is_configured(self):
        return self.provider == "ollama" or bool(self.api_key)

    def complete(self, prompt, system_prompt=None, temperature=0.3, max_tokens=2048):
        try:
            if self.provider == "ollama":
                return self._ollama(prompt, system_prompt, temperature, max_tokens)
            return self._openai_style(prompt, system_prompt, temperature, max_tokens)
        except Exception as e:
            return LLMResponse.error_response(e, self.provider)

    def _ollama(self, prompt, system_prompt, temperature, max_tokens):
        full = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        payload = {
            "model": self.model,
            "prompt": full,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }

        req = urllib.request.Request(
            f"{self.base_url}/generate",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())

        return LLMResponse(
            data.get("response", ""),
            self.model,
            self.provider,
            0
        )

    def _openai_style(self, prompt, system_prompt, temperature, max_tokens):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps({
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }).encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode())

        content = data["choices"][0]["message"]["content"]

        return LLMResponse(content, self.model, self.provider, 0)