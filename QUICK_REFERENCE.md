# VoiceFlow – Quick Reference Guide

## 🚀 Installation (30 seconds)

```bash
# Clone
git clone <your-repo-url>
cd murf-voiceflow-agent

# Setup
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your API keys to .env

# Run
python -m app.cli_runner
```

---

## 🎤 Usage

1. **Start the app:** `python -m app.cli_runner`
2. **Press Enter** to record
3. **Speak your question**
4. **Wait** for the response (2-3 seconds)
5. **Hear** the Murf Falcon voice reply
6. **Repeat** or type `q` to quit

---

## 🔧 Configuration

Edit `.env` file:

```dotenv
MURF_API_KEY=your_murf_api_key
DEEPGRAM_API_KEY=your_deepgram_key
OPENAI_API_KEY=your_openai_key
```

Optional settings:
- `MURF_REGION` - GLOBAL (default), IN, US
- `MURF_VOICE_ID` - Matthew (default), others available
- `OPENAI_MODEL` - gpt-4o-mini (default), gpt-4, gpt-4-turbo
- `SAMPLE_RATE` - 16000 (default)
- `LOG_LEVEL` - INFO (default), DEBUG, WARNING
- `MAX_RETRIES` - 3 (default)
- `REQUEST_TIMEOUT` - 60 (default)

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html

# Run specific test
pytest tests/test_agent.py -v
```

---

## 🐳 Docker

```bash
# Build
docker build -t voiceflow:latest .

# Run
docker run -it \
  -e MURF_API_KEY=xxx \
  -e DEEPGRAM_API_KEY=xxx \
  -e OPENAI_API_KEY=xxx \
  voiceflow:latest
```

---

## 📊 Logging

Check logs in `voiceflow.log`:

```
2025-12-08 10:23:45 - voiceflow - INFO - Recording started
2025-12-08 10:23:49 - voiceflow - INFO - Transcribed: "What is...?"
2025-12-08 10:23:52 - voiceflow - INFO - LLM response generated
2025-12-08 10:23:54 - voiceflow - INFO - TTS streaming complete
```

Enable debug logging:
```bash
LOG_LEVEL=DEBUG python -m app.cli_runner
```

---

## 🐛 Troubleshooting

### Error: "MURF_API_KEY is not set"
- **Solution:** Check `.env` file has `MURF_API_KEY=<your-key>`

### Error: "Microphone not detected"
- **Solution:** Check mic is connected, restart terminal
- **Debug:** `LOG_LEVEL=DEBUG python -m app.cli_runner`

### Error: "API key invalid"
- **Solution:** Verify keys in console dashboards (Murf, Deepgram, OpenAI)

### Error: "Timeout"
- **Solution:** Increase `REQUEST_TIMEOUT` in `.env` (default: 60)

### Error: "Connection refused"
- **Solution:** Check internet connection, API service status

---

## 📚 Project Structure

```
app/
├── config.py        → Configuration (edit .env, not this!)
├── logger.py        → Logging setup
├── asr_deepgram.py  → Speech-to-Text (Deepgram)
├── tts_murf.py      → Text-to-Speech (Murf)
├── llm_openai.py    → LLM (OpenAI)
├── agent.py         → Main agent logic
├── cli_runner.py    → CLI interface (what you run!)
└── utils/
    ├── exceptions.py → Custom errors
    ├── retry.py      → Retry logic
    └── audio.py      → Audio utilities

tests/               → Test suite
demo/               → Demo video & instructions
```

---

## 📞 Get Help

1. **Check** `TROUBLESHOOTING.md` for common issues
2. **Read** `DEVELOPMENT.md` for setup details
3. **Review** code comments in `app/` for implementation details
4. **Run tests** with `LOG_LEVEL=DEBUG`

---

## 🎯 Performance

- **Response Time:** 2-3 seconds (ASR + LLM + TTS)
- **Memory:** ~150MB idle, ~300MB active
- **CPU:** Minimal (I/O bound)
- **Audio Quality:** 16kHz mono (optimal for ASR)

---

## 🔐 Security Checklist

- ✅ Never commit `.env` file
- ✅ Use `.env.example` for template
- ✅ Rotate API keys regularly
- ✅ Don't share API keys in logs
- ✅ Use HTTPS (handled by libraries)

---

## 🚀 Deployment

### Local
```bash
python -m app.cli_runner
```

### Production Server
```bash
# Install
pip install -r requirements.txt

# Run with nohup
nohup python -m app.cli_runner > voiceflow.log 2>&1 &

# Or use systemd service
```

### Docker
```bash
docker build -t voiceflow .
docker run -it voiceflow
```

---

## 📖 Documentation Files

- `README.md` - Complete documentation
- `CONTRIBUTING.md` - How to contribute
- `DEVELOPMENT.md` - Development setup
- `TROUBLESHOOTING.md` - Common issues
- `PROJECT_STATUS.md` - Project status & checklist
- `QUICK_REFERENCE.md` - This file!

---

## 💡 Tips & Tricks

**Faster recording:** Increase silence detection
```bash
SILENCE_DURATION=1 python -m app.cli_runner
```

**Better accuracy:** Use larger model
```bash
OPENAI_MODEL=gpt-4 python -m app.cli_runner
```

**Better voices:** Check available Murf voice IDs
```bash
MURF_VOICE_ID=Evan python -m app.cli_runner
```

**Debug mode:** See all logs
```bash
LOG_LEVEL=DEBUG python -m app.cli_runner
```

---

## 🎓 Learn More

- [Murf AI Docs](https://murf.ai/docs)
- [Deepgram Docs](https://developers.deepgram.com)
- [OpenAI Docs](https://platform.openai.com/docs)
- [PyAudio Docs](http://people.csail.mit.edu/hubert/pyaudio)

---

**Happy voice assistant building! 🚀**
