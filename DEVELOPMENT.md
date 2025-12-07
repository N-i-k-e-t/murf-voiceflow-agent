# Development Guide

## Architecture

VoiceFlow follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────┐
│           CLI Interface (cli_runner.py)             │
├─────────────────────────────────────────────────────┤
│                 Voice Agent (agent.py)              │
├──────────────┬──────────────────────┬───────────────┤
│ ASR Client   │   LLM Client         │  TTS Client   │
│(Deepgram)    │   (OpenAI)           │  (Murf)       │
├──────────────┼──────────────────────┼───────────────┤
│    Config (config.py) - Environment & Validation    │
└─────────────────────────────────────────────────────┘
```

## Module Descriptions

### config.py
- Loads environment variables from `.env`
- Validates configuration values
- Provides defaults for optional settings
- Ensures API keys are present

### asr_deepgram.py
- Handles speech-to-text conversion
- Implements HTTP retry logic
- Manages API sessions efficiently
- Returns transcribed text

### tts_murf.py
- Handles text-to-speech streaming
- Validates input text length
- Streams audio chunks for real-time playback
- Handles API errors gracefully

### llm_openai.py
- Manages conversation with OpenAI API
- Implements retry logic for transient failures
- Maintains conversation history
- Enforces token and history limits

### agent.py
- Orchestrates ASR → LLM → TTS pipeline
- Maintains conversation context
- Manages response generation
- Handles conversation reset

### cli_runner.py
- User interface and interaction loop
- Audio recording from microphone
- Audio playback to speakers
- Status feedback and error reporting

## Key Design Patterns

### 1. Error Handling
- Every external API call has try-except
- Errors logged with appropriate level
- Graceful degradation when possible
- User-friendly error messages

### 2. Configuration Validation
- Environment variables validated at startup
- Type conversion with error handling
- Range checking for numeric values
- Safe defaults provided

### 3. Retry Logic
- Exponential backoff for transient failures
- Configurable retry counts and delays
- Different handling for different error types
- Rate limit respect

### 4. Resource Management
- Proper cleanup of audio streams
- Session management for HTTP
- Exception handling in finally blocks
- No resource leaks

### 5. Logging
- Structured logging at all levels
- Debug logs for detailed tracing
- Info logs for major milestones
- Error logs with stack traces
- Configurable log level

## Testing Strategy

### Unit Tests
Test individual modules in isolation:
```bash
pytest tests/test_config.py -v
pytest tests/test_asr.py -v
pytest tests/test_agent.py -v
```

### Coverage Analysis
```bash
pytest --cov=app/ --cov-report=html tests/
```

### Running All Tests
```bash
pytest tests/ -v --cov=app/
```

## Performance Optimization

### Audio Processing
- Chunk size optimization (1024 bytes)
- Non-blocking audio recording
- Efficient WAV encoding

### API Calls
- Connection pooling via requests.Session
- Appropriate timeouts
- Retry logic to reduce failures

### Memory
- Stream audio instead of buffering entire file
- Iterator-based chunk processing
- Conversation history limits

## Debugging

### Enable Debug Logging
```bash
export LOG_LEVEL=DEBUG
python -m app.cli_runner
```

### Check API Keys
```python
from app import config
print(f"MURF_API_KEY: {bool(config.MURF_API_KEY)}")
print(f"DEEPGRAM_API_KEY: {bool(config.DEEPGRAM_API_KEY)}")
print(f"OPENAI_API_KEY: {bool(config.OPENAI_API_KEY)}")
```

### Test Individual Components
```python
from app.asr_deepgram import DeepgramASRClient
from app.tts_murf import MurfTTSClient
from app.llm_openai import LLMClient

asr = DeepgramASRClient()
tts = MurfTTSClient()
llm = LLMClient()
```

## Common Issues

### 1. Microphone Not Detected
- Check system audio settings
- List devices: `python -c "import pyaudio; p=pyaudio.PyAudio(); [print(i, p.get_device_info_by_index(i)) for i in range(p.get_device_count())]"`
- Specify device in config

### 2. API Authentication Failures
- Verify API keys are correct
- Check .env file exists and is readable
- Ensure no typos in environment variable names
- Verify API keys have required permissions

### 3. Audio Quality Issues
- Adjust SAMPLE_RATE (16000 is standard)
- Check microphone hardware
- Reduce background noise
- Increase RECORD_SECONDS if needed

### 4. Timeout Errors
- Increase REQUEST_TIMEOUT in .env
- Check internet connection
- Verify API endpoints are accessible
- Check API rate limits

## Code Style Guide

### Python Style
Follow PEP 8 standards:
```bash
black app/ tests/  # Auto-format
flake8 app/ tests/  # Check style
```

### Type Hints
Use type hints for clarity:
```python
def process_text(text: str) -> Optional[str]:
    """Process and validate text."""
    return text.strip() if text else None
```

### Docstrings
Use Google-style docstrings:
```python
def function_name(param1: str, param2: int) -> bool:
    """One-line summary.
    
    Longer description explaining what this
    function does and why.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param2 is negative
    """
```

### Comments
Comment complex logic and important decisions:
```python
# Validate text length to prevent API errors
if len(text) > MAX_TEXT_LENGTH:
    text = text[:MAX_TEXT_LENGTH]
```

## Building for Production

### 1. Testing
```bash
pytest tests/ -v --cov=app/ --cov-fail-under=80
```

### 2. Linting
```bash
flake8 app/ --count --select=E9,F63,F7,F82 --show-source --statistics
```

### 3. Type Checking
```bash
mypy app/ --strict
```

### 4. Security
```bash
# Check for common security issues
bandit -r app/
```

### 5. Build Package
```bash
python setup.py sdist bdist_wheel
```

## Deployment

### Docker (Optional)
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app/ ./app/
CMD ["python", "-m", "app.cli_runner"]
```

### Environment Setup
1. Set API keys as environment variables
2. Configure audio device selection
3. Set log level for production
4. Enable monitoring/observability

## Performance Metrics

Monitor these metrics:
- API response times
- Transcription accuracy
- Audio quality (frequency/SNR)
- Error rates
- Memory usage
- CPU utilization

## Future Enhancements

Potential improvements:
- [ ] Add GUI interface
- [ ] Support multiple languages
- [ ] Real-time transcription display
- [ ] Conversation export/logging
- [ ] Custom voice profiles
- [ ] Local ASR/TTS fallbacks
- [ ] Advanced error recovery
- [ ] Performance profiling

## References

- [Murf API Docs](https://murf.ai/docs)
- [Deepgram API Docs](https://developers.deepgram.com)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Python Best Practices](https://peps.python.org/pep-0008/)
