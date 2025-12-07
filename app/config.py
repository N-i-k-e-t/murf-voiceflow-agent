import os
import logging
from dotenv import load_dotenv

# Initialize logging
logger = logging.getLogger(__name__)

# Load environment variables from .env file if present
load_dotenv()


def _validate_env_var(key: str, required: bool = True, default: str = None) -> str:
    """Validate and retrieve environment variable with proper error handling."""
    value = os.getenv(key, default)
    if required and not value:
        raise RuntimeError(
            f"Missing required environment variable: {key}. "
            f"Please set it in .env file or as a system environment variable."
        )
    if value is None:
        value = default
    return value


def _validate_positive_int(key: str, default: int) -> int:
    """Validate environment variable is a positive integer."""
    try:
        value = int(os.getenv(key, default))
        if value <= 0:
            raise ValueError(f"{key} must be positive")
        return value
    except ValueError as e:
        logger.warning(f"Invalid {key} value: {e}. Using default {default}")
        return default


# API Keys (required)
MURF_API_KEY = _validate_env_var("MURF_API_KEY", required=True)
DEEPGRAM_API_KEY = _validate_env_var("DEEPGRAM_API_KEY", required=True)
OPENAI_API_KEY = _validate_env_var("OPENAI_API_KEY", required=True)

# Murf Falcon TTS Configuration
MURF_REGION = _validate_env_var("MURF_REGION", required=False, default="GLOBAL")
MURF_VOICE_ID = _validate_env_var("MURF_VOICE_ID", required=False, default="Matthew")
VALID_REGIONS = {"GLOBAL", "IN", "US", "EU", "AP"}
if MURF_REGION not in VALID_REGIONS:
    logger.warning(
        f"Invalid MURF_REGION: {MURF_REGION}. Using GLOBAL. Valid: {VALID_REGIONS}"
    )
    MURF_REGION = "GLOBAL"

# OpenAI Configuration
OPENAI_MODEL = _validate_env_var("OPENAI_MODEL", required=False, default="gpt-4o-mini")
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
if not 0 <= OPENAI_TEMPERATURE <= 2:
    logger.warning(f"Invalid temperature {OPENAI_TEMPERATURE}. Using 0.7")
    OPENAI_TEMPERATURE = 0.7

# Audio settings
SAMPLE_RATE = _validate_positive_int("SAMPLE_RATE", 16000)
CHANNELS = 1
RECORD_SECONDS = _validate_positive_int("RECORD_SECONDS", 5)
MAX_RECORD_SECONDS = 60  # safety limit
if RECORD_SECONDS > MAX_RECORD_SECONDS:
    logger.warning(
        f"RECORD_SECONDS too high ({RECORD_SECONDS}). Capping at {MAX_RECORD_SECONDS}"
    )
    RECORD_SECONDS = MAX_RECORD_SECONDS

# Request/Retry Configuration
REQUEST_TIMEOUT = _validate_positive_int("REQUEST_TIMEOUT", 60)
MAX_RETRIES = _validate_positive_int("MAX_RETRIES", 3)
RETRY_DELAY = _validate_positive_int("RETRY_DELAY", 1)

# Logging Configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
if LOG_LEVEL not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
    LOG_LEVEL = "INFO"

logger.debug(f"Configuration loaded: MURF_REGION={MURF_REGION}, OPENAI_MODEL={OPENAI_MODEL}")
