"""Tests for TTS (Murf) module."""

import pytest
from unittest.mock import Mock, patch
from app.tts_murf import MurfTTSClient
from app.utils.exceptions import TTSError


def test_murf_client_initialization():
    """Test MurfTTSClient initialization."""
    with patch.dict("os.environ", {"MURF_API_KEY": "test_key"}):
        with patch("app.tts_murf.Murf"):
            client = MurfTTSClient()
            assert client is not None


def test_murf_client_missing_key():
    """Test MurfTTSClient without API key."""
    with patch.dict("os.environ", {"MURF_API_KEY": ""}, clear=True):
        with pytest.raises(RuntimeError):
            MurfTTSClient()
