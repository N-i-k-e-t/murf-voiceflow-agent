import logging
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import DEEPGRAM_API_KEY, REQUEST_TIMEOUT, MAX_RETRIES, RETRY_DELAY

logger = logging.getLogger(__name__)


class DeepgramASRClient:
    """Robust Deepgram STT client for WAV audio with retry logic."""

    def __init__(self) -> None:
        if not DEEPGRAM_API_KEY:
            raise RuntimeError("DEEPGRAM_API_KEY is not set")
        
        self.base_url = "https://api.deepgram.com/v1/listen"
        self.session = self._create_session()
        logger.info("DeepgramASRClient initialized")

    def _create_session(self) -> requests.Session:
        """Create a requests session with automatic retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["POST"],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def transcribe_wav(
        self, wav_bytes: bytes, model: str = "nova-3"
    ) -> Optional[str]:
        """
        Send WAV audio bytes to Deepgram and return transcript text.
        
        Args:
            wav_bytes: Raw WAV audio data
            model: Deepgram model to use (default: nova-3)
            
        Returns:
            Transcript text or None if transcription failed
        """
        if not wav_bytes:
            logger.warning("Empty audio bytes provided to transcribe_wav")
            return None

        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav",
        }
        params = {
            "model": model,
            "smart_format": "true",
            "punctuate": "true",
            "paragraphs": "true",
        }

        try:
            logger.debug(f"Sending audio to Deepgram (model={model})")
            resp = self.session.post(
                self.base_url,
                headers=headers,
                params=params,
                data=wav_bytes,
                timeout=REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            
            transcript = (
                data["results"]["channels"][0]["alternatives"][0]["transcript"].strip()
            )
            
            if not transcript:
                logger.warning("Empty transcript received from Deepgram")
                return None
            
            logger.debug(f"Transcript: {transcript[:100]}...")
            return transcript
            
        except requests.exceptions.Timeout:
            logger.error(f"Deepgram request timeout after {REQUEST_TIMEOUT}s")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Deepgram connection error: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Deepgram HTTP error: {resp.status_code} - {resp.text}")
            return None
        except (KeyError, IndexError, ValueError) as e:
            logger.error(f"Failed to parse Deepgram response: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in transcribe_wav: {e}")
            return None
