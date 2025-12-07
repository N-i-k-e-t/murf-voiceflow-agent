import logging
from typing import List, Dict, Optional

from openai import OpenAI, APIError, APIConnectionError, RateLimitError  # type: ignore

from .config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_TEMPERATURE,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
)

logger = logging.getLogger(__name__)

# Safety limits
MAX_TOKENS = 512
MAX_CONVERSATION_HISTORY = 20


class LLMClient:
    """Robust OpenAI Chat Completions API client with retry and timeout logic."""

    def __init__(self) -> None:
        if not OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY is not set")
        
        try:
            self.client = OpenAI(api_key=OPENAI_API_KEY, timeout=REQUEST_TIMEOUT)
            self.model = OPENAI_MODEL
            logger.info(f"LLMClient initialized with model={self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {e}")
            raise RuntimeError(f"OpenAI initialization failed: {e}")

    def chat(
        self, messages: List[Dict[str, str]], max_retries: int = MAX_RETRIES
    ) -> Optional[str]:
        """
        Send conversation and return assistant reply text.
        Implements retry logic for transient failures.
        
        Args:
            messages: Conversation history with role/content
            max_retries: Number of retries on failure
            
        Returns:
            Assistant response or None if all retries failed
        """
        if not messages:
            logger.warning("Empty message list provided to chat")
            return None
        
        # Validate messages
        if len(messages) > MAX_CONVERSATION_HISTORY:
            logger.warning(
                f"Conversation history too long ({len(messages)} msgs). "
                f"Keeping last {MAX_CONVERSATION_HISTORY//2} exchanges."
            )
            # Keep system message + last N exchanges
            system_msg = [m for m in messages if m.get("role") == "system"]
            other_msgs = [m for m in messages if m.get("role") != "system"]
            messages = system_msg + other_msgs[-(MAX_CONVERSATION_HISTORY - 2) :]
        
        for attempt in range(max_retries + 1):
            try:
                logger.debug(f"Chat API call (attempt {attempt + 1}/{max_retries + 1})")
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=OPENAI_TEMPERATURE,
                    max_tokens=MAX_TOKENS,
                )
                
                response = completion.choices[0].message.content.strip()
                
                if not response:
                    logger.warning("Empty response from OpenAI")
                    return None
                
                logger.debug(f"LLM response: {response[:100]}...")
                return response
                
            except RateLimitError as e:
                logger.warning(f"Rate limited. Attempt {attempt + 1}/{max_retries + 1}")
                if attempt == max_retries:
                    logger.error("Max retries exceeded for rate limit")
                    return None
                
            except APIConnectionError as e:
                logger.warning(f"Connection error. Attempt {attempt + 1}/{max_retries + 1}: {e}")
                if attempt == max_retries:
                    logger.error("Max retries exceeded for connection error")
                    return None
                    
            except APIError as e:
                logger.error(f"OpenAI API error: {e}")
                if attempt == max_retries:
                    return None
                    
            except Exception as e:
                logger.error(f"Unexpected error in chat: {e}")
                return None
        
        return None
