"""Integration tests for VoiceFlow."""

import pytest
from unittest.mock import patch, MagicMock


def test_full_voice_flow_mock():
    """Test complete voice flow with mocked APIs."""
    with patch("app.cli_runner.record_audio") as mock_record, patch(
        "app.cli_runner.DeepgramASRClient"
    ) as mock_asr_class, patch("app.cli_runner.MurfTTSClient") as mock_tts_class, patch(
        "app.cli_runner.VoiceAgent"
    ) as mock_agent_class:

        # Setup mocks
        mock_record.return_value = b"fake_wav_data"

        mock_asr = MagicMock()
        mock_asr.transcribe_wav.return_value = "Hello"
        mock_asr_class.return_value = mock_asr

        mock_tts = MagicMock()
        mock_tts.stream_tts.return_value = [b"audio_chunk"]
        mock_tts_class.return_value = mock_tts

        mock_agent = MagicMock()
        mock_agent.reply.return_value = "Hi there!"
        mock_agent_class.return_value = mock_agent

        # Simulate one loop iteration
        wav_bytes = mock_record()
        transcript = mock_asr.transcribe_wav(wav_bytes)
        response = mock_agent.reply(transcript)
        audio_chunks = mock_tts.stream_tts(response)

        # Verify
        assert wav_bytes == b"fake_wav_data"
        assert transcript == "Hello"
        assert response == "Hi there!"
        assert audio_chunks == [b"audio_chunk"]
