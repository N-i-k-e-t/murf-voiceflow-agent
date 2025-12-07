import logging
from typing import List, Dict, Optional

from .llm_openai import LLMClient

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are VoiceFlow, a helpful, concise voice assistant. "
    "User is speaking, so keep responses short and clear, "
    "ideally 1–3 sentences. You can help with quick explanations, "
    "task notes, and simple Q&A. Be professional and informative."
)

# Conversation state management
MAX_HISTORY_LENGTH = 50


class VoiceAgent:
    """High-level agent that turns transcripts into reply text with conversation memory."""

    def __init__(self) -> None:
        self.llm = LLMClient()
        self.history: List[Dict[str, str]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        logger.info("VoiceAgent initialized")

    def reply(self, user_text: str) -> Optional[str]:
        """
        Process user input and generate agent reply.
        
        Args:
            user_text: User's input text
            
        Returns:
            Agent's response or None if generation failed
        """
        if not user_text or not user_text.strip():
            logger.warning("Empty user text provided to reply")
            return None
        
        user_text = user_text.strip()
        
        # Prevent history from growing unbounded
        if len(self.history) > MAX_HISTORY_LENGTH:
            logger.debug(f"Trimming conversation history from {len(self.history)} to 20 messages")
            # Keep system prompt + recent history
            system_msg = self.history[0]
            recent = self.history[-(MAX_HISTORY_LENGTH - 10) :]
            self.history = [system_msg] + recent
        
        try:
            self.history.append({"role": "user", "content": user_text})
            logger.debug(f"User: {user_text[:100]}...")
            
            answer = self.llm.chat(self.history)
            
            if not answer:
                logger.error("LLM failed to generate response")
                # Remove the user message we just added since we got no response
                self.history.pop()
                return None
            
            self.history.append({"role": "assistant", "content": answer})
            logger.debug(f"Agent: {answer[:100]}...")
            return answer
            
        except Exception as e:
            logger.error(f"Error in reply generation: {e}")
            # Clean up failed message
            if self.history and self.history[-1].get("role") == "user":
                self.history.pop()
            return None

    def reset_conversation(self) -> None:
        """Clear conversation history and start fresh."""
        logger.info("Resetting conversation history")
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
