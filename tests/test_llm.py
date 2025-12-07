"""Tests for LLM (OpenAI) module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from app.llm_openai import LLMClient


def test_llm_client_initialization():
    """Test LLMClient initialization."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test_key"}):
        with patch("app.llm_openai.OpenAI"):
            client = LLMClient()
            assert client is not None


def test_llm_client_missing_key():
    """Test LLMClient without API key."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": ""}, clear=True):
        with pytest.raises(RuntimeError):
            LLMClient()


def test_llm_chat():
    """Test LLMClient chat method."""
    with patch.dict("os.environ", {"OPENAI_API_KEY": "test_key"}):
        with patch("app.llm_openai.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client

            mock_response = MagicMock()
            mock_response.choices[0].message.content = "Test response"
            mock_client.chat.completions.create.return_value = mock_response

            client = LLMClient()
            response = client.chat([{"role": "user", "content": "Hello"}])

            assert response == "Test response"
