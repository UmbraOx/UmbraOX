import pytest
from core.runtime.runtime_llm_provider import RuntimeLLMProvider


def test_groq_uses_openai_compatible_format():
    provider = RuntimeLLMProvider(provider="groq", api_key="gsk_test")
    assert "groq.com" in provider.base_url


def test_groq_default_model_is_llama():
    provider = RuntimeLLMProvider(provider="groq", model="llama3-8b-8192", api_key="gsk_test")
    assert "llama" in provider.get_model()


def test_groq_is_configured_with_key():
    provider = RuntimeLLMProvider(provider="groq", api_key="gsk_test")
    assert provider.is_configured() is True


def test_groq_not_configured_without_key():
    provider = RuntimeLLMProvider(provider="groq", api_key="")
    assert provider.is_configured() is False


def test_groq_is_free():
    provider = RuntimeLLMProvider(provider="groq", api_key="key")
    assert provider.is_free() is True


def test_groq_custom_model():
    provider = RuntimeLLMProvider(provider="groq", model="mixtral-8x7b-32768", api_key="key")
    assert provider.get_model() == "mixtral-8x7b-32768"