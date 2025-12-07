"""Custom exceptions for VoiceFlow."""


class VoiceFlowException(Exception):
    """Base exception for VoiceFlow."""

    pass


class ConfigurationError(VoiceFlowException):
    """Raised when configuration is invalid."""

    pass


class AudioError(VoiceFlowException):
    """Raised when audio recording/playback fails."""

    pass


class ASRError(VoiceFlowException):
    """Raised when speech-to-text fails."""

    pass


class TTSError(VoiceFlowException):
    """Raised when text-to-speech fails."""

    pass


class LLMError(VoiceFlowException):
    """Raised when LLM inference fails."""

    pass


class APIError(VoiceFlowException):
    """Raised when API call fails after retries."""

    pass
