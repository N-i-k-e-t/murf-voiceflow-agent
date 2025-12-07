"""Pytest configuration and shared fixtures."""
import os
import pytest
from unittest.mock import MagicMock, patch

# Set test environment variables
os.environ["MURF_API_KEY"] = "test_murf_key"
os.environ["DEEPGRAM_API_KEY"] = "test_deepgram_key"
os.environ["OPENAI_API_KEY"] = "test_openai_key"


@pytest.fixture
def mock_murf_client():
    """Mock Murf TTS client."""
    with patch("app.tts_murf.Murf") as mock:
        mock.return_value.text_to_speech.stream.return_value = iter([b"audio_chunk_1", b"audio_chunk_2"])
        yield mock


@pytest.fixture
def mock_deepgram_session():
    """Mock Deepgram API session."""
    with patch("app.asr_deepgram.requests.Session") as mock:
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "results": {
                "channels": [
                    {
                        "alternatives": [
                            {"transcript": "Hello, how are you?"}
                        ]
                    }
                ]
            }
        }
        mock.return_value.post.return_value = mock_response
        yield mock


@pytest.fixture
def mock_openai_client():
    """Mock OpenAI API client."""
    with patch("app.llm_openai.OpenAI") as mock:
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "I'm doing great, thanks for asking!"
        mock.return_value.chat.completions.create.return_value = mock_response
        yield mock
