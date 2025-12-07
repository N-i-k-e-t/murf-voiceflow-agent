"""Tests for VoiceAgent module."""
import pytest
from unittest.mock import MagicMock, patch
from app.agent import VoiceAgent, SYSTEM_PROMPT


def test_agent_initialization(mock_openai_client):
    """Test VoiceAgent initialization."""
    agent = VoiceAgent()
    assert agent.history is not None
    assert len(agent.history) == 1
    assert agent.history[0]["role"] == "system"
    assert agent.history[0]["content"] == SYSTEM_PROMPT


def test_agent_reply(mock_openai_client):
    """Test agent reply generation."""
    with patch("app.agent.LLMClient") as mock_llm:
        mock_llm.return_value.chat.return_value = "Hello! How can I help?"
        
        agent = VoiceAgent()
        agent.llm = mock_llm.return_value
        
        response = agent.reply("Hi there")
        
        assert response == "Hello! How can I help?"
        assert len(agent.history) == 3  # system + user + assistant


def test_agent_reply_empty_text():
    """Test agent reply with empty text."""
    with patch("app.agent.LLMClient"):
        agent = VoiceAgent()
        result = agent.reply("")
        assert result is None
        
        result = agent.reply("   ")
        assert result is None


def test_agent_reply_llm_failure():
    """Test agent reply when LLM fails."""
    with patch("app.agent.LLMClient") as mock_llm:
        mock_llm.return_value.chat.return_value = None
        
        agent = VoiceAgent()
        agent.llm = mock_llm.return_value
        
        result = agent.reply("Hi")
        assert result is None


def test_agent_history_limit():
    """Test that conversation history doesn't grow unbounded."""
    from app.agent import MAX_HISTORY_LENGTH
    
    with patch("app.agent.LLMClient") as mock_llm:
        mock_llm.return_value.chat.return_value = "Response"
        
        agent = VoiceAgent()
        agent.llm = mock_llm.return_value
        
        # Add many messages
        for i in range(MAX_HISTORY_LENGTH + 10):
            agent.reply(f"Message {i}")
        
        # History should be trimmed
        assert len(agent.history) <= MAX_HISTORY_LENGTH + 5


def test_agent_reset_conversation(mock_openai_client):
    """Test conversation reset."""
    with patch("app.agent.LLMClient") as mock_llm:
        mock_llm.return_value.chat.return_value = "Response"
        
        agent = VoiceAgent()
        agent.llm = mock_llm.return_value
        
        agent.reply("Test message")
        assert len(agent.history) > 1
        
        agent.reset_conversation()
        assert len(agent.history) == 1
        assert agent.history[0]["role"] == "system"
