# Troubleshooting Guide

## Common Issues and Solutions

### Installation Issues

#### 1. PyAudio Installation Fails

**Problem:** `error: Microsoft Visual C++ 14.0 is required`

**Solutions:**
- **Windows:** Download and install [Build Tools for Visual Studio 2022](https://visualstudio.microsoft.com/downloads/)
- **macOS:** `brew install portaudio && pip install pyaudio`
- **Linux:** `sudo apt-get install python3-pyaudio`

#### 2. Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'murf'`

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

#### 3. .env File Not Loading

**Problem:** Environment variables not set

**Solution:**
```bash
# Verify .env file exists
ls -la .env

# Check format (no quotes around values)
cat .env | grep MURF_API_KEY

# Reload with absolute path
export $(cat /absolute/path/to/.env | xargs)
```

### API Issues

#### 4. Authentication Failures

**Problem:** `APIError: Unauthorized` or `Invalid API key`

**Solution:**
```bash
# Verify API key format
echo $MURF_API_KEY
echo $DEEPGRAM_API_KEY
echo $OPENAI_API_KEY

# Check for extra whitespace
python -c "import os; print(repr(os.getenv('MURF_API_KEY')))"

# Test API connectivity
python -c "
from app.config import *
from app.asr_deepgram import DeepgramASRClient
try:
    client = DeepgramASRClient()
    print('✓ Deepgram connected')
except Exception as e:
    print(f'✗ Deepgram error: {e}')
"
```

#### 5. Rate Limiting

**Problem:** `429 Too Many Requests` errors

**Solution:**
```bash
# Increase retry delay
export RETRY_DELAY=2
export MAX_RETRIES=5

# Reduce request frequency
# Add delays between requests
```

#### 6. Connection Timeouts

**Problem:** `ConnectTimeout` or `ReadTimeout`

**Solution:**
```bash
# Increase timeout
export REQUEST_TIMEOUT=120

# Check network
ping api.deepgram.com
ping api.openai.com

# Check for proxy requirements
# Configure system proxy if needed
```

### Audio Issues

#### 7. Microphone Not Detected

**Problem:** `OSError: [Errno -1] Unanticipated host error` or no audio input

**Solution:**
```bash
# List available audio devices
python << 'EOF'
import pyaudio
p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(f"Device {i}: {info['name']} (Channels: {info['maxInputChannels']})")
p.terminate()
EOF

# Test specific device
export AUDIO_DEVICE_INDEX=0

# Check system audio
# Windows: Settings > Sound > Input devices
# macOS: System Preferences > Sound > Input
# Linux: pacmd list-sources or alsamixer
```

#### 8. Poor Audio Quality

**Problem:** Transcription errors, "audio not understood"

**Solution:**
```bash
# Increase recording time
export RECORD_SECONDS=10

# Reduce background noise
# - Use headset/quality microphone
# - Move away from fans, traffic
# - Close browser tabs

# Verify audio format
python << 'EOF'
from app.cli_runner import record_audio
import wave
wav_bytes = record_audio()
with wave.open("test_audio.wav", "wb") as f:
    f.write(wav_bytes)
# Listen to test_audio.wav
EOF

# Change sample rate if needed
export SAMPLE_RATE=16000  # Standard
# or
export SAMPLE_RATE=8000   # For bandwidth-limited connections
```

#### 9. No Audio Output

**Problem:** Agent responds but no speech output

**Solution:**
```bash
# Check speakers
# - Verify speakers are connected
# - Check volume level
# - Test system audio

# Check Murf TTS
python << 'EOF'
from app.tts_murf import MurfTTSClient
tts = MurfTTSClient()
chunks = tts.stream_tts("Hello, this is a test")
if chunks:
    print("✓ TTS working, saving to file...")
    with open("test_output.wav", "wb") as f:
        for chunk in chunks:
            if chunk:
                f.write(chunk)
else:
    print("✗ TTS failed")
EOF

# Play test file
# Windows: start test_output.wav
# macOS: open test_output.wav
# Linux: play test_output.wav
```

### Performance Issues

#### 10. High Latency

**Problem:** Slow response times between stages

**Solution:**
```bash
# Enable debug logging
export LOG_LEVEL=DEBUG
python -m app.cli_runner 2>&1 | tee debug.log

# Analyze log timestamps
grep "Recording finished\|Transcribing\|Generating\|Speaking" debug.log

# Profile code
python -m cProfile -s cumulative -m app.cli_runner > profile.txt

# Reduce model complexity (faster but less accurate)
export OPENAI_MODEL=gpt-3.5-turbo
```

#### 11. High Memory Usage

**Problem:** Memory grows during long sessions

**Solution:**
```bash
# Monitor memory
python -m memory_profiler app/cli_runner.py

# Limit conversation history
export MAX_HISTORY_LENGTH=20

# Clear cache periodically
```

### Windows-Specific Issues

#### 12. PyAudio Fails on Windows

**Problem:** Installation or runtime errors

**Solution:**
```bash
# Use wheel file
pip install pipwin
pipwin install pyaudio

# Or install Visual C++ Build Tools
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

# Or use alternative audio library
pip install sounddevice pydub
```

#### 13. PATH Issues

**Problem:** Scripts not found

**Solution:**
```bash
# Use full path
python -m app.cli_runner

# Or activate venv properly
.venv\Scripts\activate

# Verify Python path
python -c "import sys; print(sys.executable)"
```

### macOS-Specific Issues

#### 14. Microphone Permission Denied

**Problem:** `Permission denied` when accessing microphone

**Solution:**
```bash
# Grant microphone permission
# Settings > Security & Privacy > Microphone > Add terminal

# Or use System Preferences
# Settings > Privacy & Security > Microphone > Terminal
```

#### 15. PortAudio Not Found

**Problem:** `error: PortAudio not installed`

**Solution:**
```bash
# Install PortAudio via Homebrew
brew install portaudio

# Then install PyAudio
pip install pyaudio
```

### Linux-Specific Issues

#### 16. ALSA Warnings

**Problem:** Many ALSA error messages (usually non-fatal)

**Solution:**
```bash
# Suppress ALSA warnings
python -W ignore -m app.cli_runner

# Or configure ALSA
# Edit ~/.asoundrc with proper configuration
```

#### 17. PulseAudio Issues

**Problem:** Audio device errors with PulseAudio

**Solution:**
```bash
# Check PulseAudio status
pulseaudio --version
pacmd list-sinks

# Restart PulseAudio
pulseaudio -k
pulseaudio --start

# Use ALSA backend
export AUDIODEV=hw:0
```

## Debugging Techniques

### 1. Enable Verbose Logging

```bash
export LOG_LEVEL=DEBUG
python -m app.cli_runner > debug.log 2>&1
```

### 2. Test Individual Components

```python
# Test configuration
from app import config
print(f"Config loaded: {config.OPENAI_MODEL}")

# Test ASR
from app.asr_deepgram import DeepgramASRClient
asr = DeepgramASRClient()

# Test TTS
from app.tts_murf import MurfTTSClient
tts = MurfTTSClient()

# Test LLM
from app.llm_openai import LLMClient
llm = LLMClient()
```

### 3. Check API Credentials

```bash
curl -H "Authorization: Token $DEEPGRAM_API_KEY" https://api.deepgram.com/v1/models
curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
```

### 4. Monitor Network

```bash
# macOS/Linux
tcpdump -i any -n "port 443"

# Windows
netsh trace start capture=yes tracefile=capture.etl
netsh trace stop
```

## Getting Help

1. **Check logs:** Look for detailed error messages
2. **Search issues:** https://github.com/your-repo/issues
3. **Read documentation:** Check DEVELOPMENT.md and README.md
4. **Ask community:** Create GitHub discussion
5. **Report bug:** Create GitHub issue with:
   - Python version
   - OS and version
   - Complete error message
   - Steps to reproduce
   - Debug logs (with API keys removed)

## Performance Baseline

Expected performance on modern hardware:
- Audio recording: < 100ms overhead
- Transcription: 2-5 seconds (depends on audio length)
- LLM response: 1-3 seconds
- TTS synthesis: 1-2 seconds
- **Total latency:** ~5-12 seconds per exchange

## Error Codes Reference

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Unauthorized | Check API key |
| 429 | Rate limited | Increase retry delay |
| 500 | Server error | Retry after delay |
| 503 | Service unavailable | Wait and retry |
| Timeout | Connection timeout | Increase REQUEST_TIMEOUT |

## Healthy System Checklist

- [ ] API keys configured correctly
- [ ] Microphone detected and working
- [ ] Speakers detected and working
- [ ] Network connectivity verified
- [ ] All dependencies installed
- [ ] Tests pass: `pytest tests/ -v`
- [ ] No errors in debug logs
- [ ] Response time acceptable
- [ ] Memory stable during use
- [ ] Audio quality satisfactory
