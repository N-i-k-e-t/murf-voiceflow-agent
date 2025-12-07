import logging
from typing import Iterable, Optional

from murf import Murf, MurfRegion  # type: ignore

from .config import MURF_API_KEY, MURF_REGION, MURF_VOICE_ID, SAMPLE_RATE

logger = logging.getLogger(__name__)

# Text length constraints for safety
MIN_TEXT_LENGTH = 1
MAX_TEXT_LENGTH = 1000


class MurfTTSClient:
    """Robust Murf Falcon streaming TTS client with error handling."""

    def __init__(self) -> None:
        if not MURF_API_KEY:
            raise RuntimeError("MURF_API_KEY is not set")
        
        # Map string region like "GLOBAL", "IN" to MurfRegion enum
        try:
            region = getattr(MurfRegion, MURF_REGION, MurfRegion.GLOBAL)
            self.client = Murf(api_key=MURF_API_KEY, region=region)
            logger.info(f"MurfTTSClient initialized (region={MURF_REGION}, voice={MURF_VOICE_ID})")
        except Exception as e:
            logger.error(f"Failed to initialize Murf client: {e}")
            raise RuntimeError(f"Murf initialization failed: {e}")

    def stream_tts(self, text: str) -> Optional[Iterable[bytes]]:
        """
        Return an iterator of audio chunks (PCM 16-bit) for the given text.
        Uses Murf Falcon with real-time streaming.
        
        Args:
            text: Text to convert to speech
            
        Returns:
            Iterator of audio chunks or None if TTS failed
        """
        # Validate input
        if not text:
            logger.warning("Empty text provided to stream_tts")
            return None
        
        text = text.strip()
        if len(text) < MIN_TEXT_LENGTH:
            logger.warning(f"Text too short: {len(text)} chars")
            return None
        
        if len(text) > MAX_TEXT_LENGTH:
            logger.warning(f"Text too long: {len(text)} chars. Truncating to {MAX_TEXT_LENGTH}")
            text = text[:MAX_TEXT_LENGTH]
        
        try:
            logger.debug(f"Streaming TTS for {len(text)} chars of text")
            audio_stream = self.client.text_to_speech.stream(
                text=text,
                voice_id=MURF_VOICE_ID,
                model="FALCON",
                multi_native_locale="en-US",
                sample_rate=SAMPLE_RATE,
                format="PCM",
            )
            logger.debug("TTS stream initiated successfully")
            return audio_stream
            
        except ValueError as e:
            logger.error(f"Invalid TTS parameters: {e}")
            return None
        except ConnectionError as e:
            logger.error(f"Murf API connection error: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in stream_tts: {e}")
            return None
