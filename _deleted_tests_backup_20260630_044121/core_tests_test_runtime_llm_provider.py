import pytest
from core.runtime.runtime_llm_provider import RuntimeLLMProvider, LLMResponse


def test_llm_provider_init_defaults():
    # Explicitly pass model to avoid UMBRA_LLM_MODEL env var interference
    provider = RuntimeLLMProvider(provider="openai", model="gpt-4o-mini", api_key="test-key")
    assert provider.get_provider() == "openai"
    assert provider.get_model() == "gpt-4o-mini"
    assert provider.is_configured() is True


def test_llm_provider_anthropic_init():
    provider = RuntimeLLMProvider(provider="anthropic", model="claude-3-5-haiku-20241022", api_key="test-key")
    assert provider.get_provider() == "anthropic"
    assert "claude" in provider.get_model()
    assert provider.is_configured() is True


def test_llm_provider_ollama_no_key():
    provider = RuntimeLLMProvider(provider="ollama")
    assert provider.is_configured() is True


def test_llm_provider_groq_init():
    provider = RuntimeLLMProvider(provider="groq", api_key="gsk_test")
    assert provider.get_provider() == "groq"
    assert provider.is_configured() is True
    assert "groq.com" in provider.base_url


def test_llm_provider_groq_default_model():
    provider = RuntimeLLMProvider(provider="groq", model="llama3-8b-8192", api_key="gsk_test")
    assert "llama" in provider.get_model()


def test_llm_provider_not_configured_without_key():
    provider = RuntimeLLMProvider(provider="openai", api_key="")
    assert provider.is_configured() is False


def test_llm_response_error():
    resp = LLMResponse.error_response("network timeout", "openai")
    assert resp.success is False
    assert resp.error == "network timeout"
    assert resp.content == ""


def test_llm_response_to_dict():
    resp = LLMResponse("hello world", "gpt-4o-mini", "openai", 42)
    d = resp.to_dict()
    assert d["content"] == "hello world"
    assert d["tokens_used"] == 42
    assert d["success"] is True


def test_llm_provider_unknown_provider_returns_error():
    provider = RuntimeLLMProvider(provider="unknown_provider", api_key="key")
    result = provider.complete("test prompt")
    assert result.success is False
    assert "Unknown provider" in result.error


def test_llm_provider_history_starts_empty():
    provider = RuntimeLLMProvider(provider="ollama")
    assert provider.get_history() == []


def test_llm_provider_custom_model():
    provider = RuntimeLLMProvider(provider="openai", model="gpt-4o", api_key="key")
    assert provider.get_model() == "gpt-4o"


def test_llm_provider_base_url_openai():
    provider = RuntimeLLMProvider(provider="openai", api_key="key")
    assert "openai.com" in provider.base_url


def test_llm_provider_base_url_anthropic():
    provider = RuntimeLLMProvider(provider="anthropic", api_key="key")
    assert "anthropic.com" in provider.base_url


def test_llm_provider_base_url_ollama():
    provider = RuntimeLLMProvider(provider="ollama")
    assert "localhost" in provider.base_url


def test_llm_provider_is_free_ollama():
    provider = RuntimeLLMProvider(provider="ollama")
    assert provider.is_free() is True


def test_llm_provider_is_free_groq():
    provider = RuntimeLLMProvider(provider="groq", api_key="key")
    assert provider.is_free() is True


def test_llm_provider_is_not_free_openai():
    provider = RuntimeLLMProvider(provider="openai", api_key="key")
    assert provider.is_free() is False