"""Tests for configuration module."""
import os
import pytest
from app import config


def test_required_env_vars():
    """Test that required environment variables are validated."""
    assert config.MURF_API_KEY == "test_murf_key"
    assert config.DEEPGRAM_API_KEY == "test_deepgram_key"
    assert config.OPENAI_API_KEY == "test_openai_key"


def test_default_values():
    """Test that default configuration values are set correctly."""
    assert config.SAMPLE_RATE == 16000
    assert config.CHANNELS == 1
    assert config.MURF_REGION == "GLOBAL"
    assert config.OPENAI_MODEL == "gpt-4o-mini"


def test_audio_limits():
    """Test that audio configuration is within safe limits."""
    assert config.RECORD_SECONDS > 0
    assert config.RECORD_SECONDS <= config.MAX_RECORD_SECONDS
    assert config.SAMPLE_RATE > 0
    assert config.CHANNELS >= 1


def test_valid_regions():
    """Test that MURF_REGION is in valid regions."""
    assert config.MURF_REGION in config.VALID_REGIONS


def test_temperature_range():
    """Test that OpenAI temperature is within valid range."""
    assert 0 <= config.OPENAI_TEMPERATURE <= 2


def test_request_config():
    """Test request and retry configuration."""
    assert config.REQUEST_TIMEOUT > 0
    assert config.MAX_RETRIES >= 0
    assert config.RETRY_DELAY >= 0
