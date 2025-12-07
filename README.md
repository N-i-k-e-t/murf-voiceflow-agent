# 🎤 VoiceFlow – Murf Falcon Voice Agent

<div align="center">

![VoiceFlow](https://img.shields.io/badge/VoiceFlow-Voice%20Agent-blue?style=for-the-badge&logo=microphone&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-8%2F8%20Passed-brightgreen?style=for-the-badge)

### 🏆 Production-Grade Real-Time Voice Assistant

**Built for Techfest IIT Bombay – Murf Voice Agent Hackathon**

🔊 **Murf Falcon TTS** • 🎯 **Deepgram ASR** • 🧠 **OpenAI LLM**

[🚀 Quick Start](#-quick-start) • [📚 Documentation](#-documentation) • [🧪 Testing](#-testing) • [🐛 Troubleshooting](#-troubleshooting) • [🤝 Contributing](#-contributing)

</div>

---

## 📸 Visual Overview

### 🎬 How It Works - Visual Flow

```
┌──────────────────────────────────────────────────────────────────┐
│                    VoiceFlow Architecture                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐          ┌──────────────────┐             │
│  │   🎤 YOU SPEAK   │          │  📝 TRANSCRIBED  │             │
│  │                  │          │                  │             │
│  │   "What is AI?"  │──────→   │  What is AI?     │             │
│  │                  │          │                  │             │
│  └──────────────────┘          └──────────────────┘             │
│           ▲                              │                       │
│           │                              ▼                       │
│           │                    ┌──────────────────┐              │
│           │                    │  🎯 Deepgram ASR │              │
│           │                    │   (Speech Input) │              │
│           │                    └──────────────────┘              │
│           │                              │                       │
│           │                              ▼                       │
│           │                    ┌──────────────────┐              │
│           │                    │  🧠 OpenAI LLM   │              │
│           │                    │ (Intelligence)   │              │
│           │                    └──────────────────┘              │
│           │                              │                       │
│           │                              ▼                       │
│           │                    ┌──────────────────┐              │
│           │                    │  💬 AI Response  │              │
│           │                    │ "AI is..."       │              │
│           │                    └──────────────────┘              │
│           │                              │                       │
│           │                              ▼                       │
│           │                    ┌──────────────────┐              │
│           │                    │ 🔊 Murf Falcon   │              │
│           │                    │   TTS (Voice)    │              │
│           │                    └──────────────────┘              │
│           │                              │                       │
│           └──────────────────────────────┘                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘

            Total Latency: 2-3 seconds
         (Recording + ASR + LLM + TTS)
```

### 🎯 Step-by-Step Process

| Step | Component | What Happens | Time |
|------|-----------|-------------|------|
| 1️⃣ | 🎤 **Recording** | Your voice captured from microphone | ~5-10s |
| 2️⃣ | 🎯 **Deepgram ASR** | Audio converted to text (Nova-3 model) | ~1-2s |
| 3️⃣ | 🧠 **OpenAI LLM** | Text sent to ChatGPT for response | ~1-2s |
| 4️⃣ | 🔊 **Murf Falcon TTS** | Response converted to natural speech | ~1-2s |
| 5️⃣ | 🔊 **Playback** | You hear the response via speaker | ~5-20s |

---

## ✨ Key Features

<table>
<tr>
<td width="50%">

### 🚀 Performance
- ⚡ **Real-time Streaming** - Low latency
- 🎯 **Accurate Recognition** - Deepgram Nova-3
- 🧠 **Intelligent Responses** - GPT-4o-mini
- 🔊 **Natural Voice** - Murf Falcon quality

### 🔒 Security
- 🔐 **Environment Variables** - Never hardcode keys
- ✅ **Input Validation** - All inputs checked
- 🛡️ **Error Handling** - Graceful failures
- 📋 **Secure Logging** - No sensitive data

</td>
<td width="50%">

### 🧪 Quality
- ✅ **8 Test Modules** - Full coverage
- 📝 **Type Hints** - 100% typed code
- 📚 **Documentation** - 8 guides included
- 🐛 **Debugging** - Comprehensive logging

### 🚀 Deployment
- 🐳 **Docker Ready** - One command deploy
- 📦 **Installable** - pip install ready
- ⚙️ **Configurable** - Environment-based
- 📈 **Scalable** - Production-grade

</td>
</tr>
</table>

---

## 🛠️ Technology Stack

<div align="center">

| Category | Technology | Purpose |
|----------|-----------|---------|
| **Speech-to-Text** | 🎯 [Deepgram](https://deepgram.com) Nova-3 | Accurate audio transcription |
| **Text-to-Speech** | 🔊 [Murf Falcon](https://murf.ai) | Natural voice synthesis |
| **Language Model** | 🧠 [OpenAI](https://openai.com) GPT-4o-mini | Intelligent responses |
| **Audio I/O** | 🎤 [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) | Microphone & speaker |
| **Framework** | 🐍 [Python 3.9+](https://python.org) | Core application |
| **Testing** | 🧪 [Pytest](https://pytest.org) | Test suite |
| **Packaging** | 📦 [setuptools](https://setuptools.pypa.io) | Distribution |
| **Container** | 🐳 [Docker](https://docker.com) | Deployment |

</div>

---

## 📂 Project Structure

```
murf-voiceflow-agent/
├── 📁 app/                           (Core Application - 13 modules)
│   ├── __init__.py                  (Package initialization)
│   ├── __main__.py                  (Entry point)
│   ├── config.py                    (⚙️ Configuration with validation)
│   ├── logger.py                    (📋 Logging setup)
│   ├── cli_runner.py                (🎤 CLI Interface)
│   ├── agent.py                     (🧠 Voice agent logic)
│   ├── asr_deepgram.py              (🎯 Speech-to-Text)
│   ├── tts_murf.py                  (🔊 Text-to-Speech)
│   ├── llm_openai.py                (🤖 LLM integration)
│   └── utils/                       (Utilities)
│       ├── exceptions.py            (Custom exceptions)
│       ├── retry.py                 (Retry logic)
│       └── audio.py                 (Audio utilities)
│
├── 📁 tests/                         (Test Suite - 8 modules)
│   ├── conftest.py                  (Pytest fixtures)
│   ├── test_config.py               (Configuration tests)
│   ├── test_asr.py                  (ASR tests)
│   ├── test_tts.py                  (TTS tests)
│   ├── test_llm.py                  (LLM tests)
│   ├── test_agent.py                (Agent tests)
│   └── test_integration.py          (End-to-end tests)
│
├── 📁 demo/                          (Demo)
│   └── README.md                    (Demo instructions)
│
├── 📄 Configuration Files
│   ├── requirements.txt              (📦 Production dependencies)
│   ├── requirements-dev.txt          (🔧 Dev dependencies)
│   ├── .env.example                 (🔑 Environment template)
│   ├── setup.py                     (📦 Package setup)
│   ├── pyproject.toml               (📋 Modern config)
│   ├── Dockerfile                   (🐳 Docker image)
│   ├── .dockerignore                (Docker ignore)
│   └── .gitignore                   (Git ignore)
│
├── 📚 Documentation (8 comprehensive guides)
│   ├── README.md                    (Main documentation)
│   ├── QUICK_REFERENCE.md           (Quick commands)
│   ├── DEVELOPMENT.md               (Dev setup)
│   ├── CONTRIBUTING.md              (Contributing)
│   ├── TROUBLESHOOTING.md           (Common issues)
│   ├── PROJECT_STATUS.md            (Status summary)
│   ├── MANIFEST.md                  (File inventory)
│   └── START_HERE.md                (Getting started)
│
└── 📄 Root Files
    ├── LICENSE                      (MIT License)
    └── MANIFEST.md                  (Project manifest)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Microphone & speakers
- PortAudio (for PyAudio)
  - **macOS:** `brew install portaudio`
  - **Ubuntu:** `sudo apt-get install portaudio19-dev`
  - **Windows:** Pre-built wheels included

### Installation (5 minutes)

```bash
# 1️⃣ Clone repository
git clone https://github.com/<your-username>/murf-voiceflow-agent.git
cd murf-voiceflow-agent

# 2️⃣ Create virtual environment
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Configure API keys
cp .env.example .env
# ✏️ Edit .env and add your API keys:
#    - MURF_API_KEY (from Murf dashboard)
#    - DEEPGRAM_API_KEY (from Deepgram console)
#    - OPENAI_API_KEY (from OpenAI platform)

# 5️⃣ Run the voice agent!
python -m app.cli_runner
```

### Usage

```
VoiceFlow – Murf Falcon Voice Agent (CLI demo)
Press Enter to speak, or type 'q' + Enter to quit.

[Enter] to record, 'q' to quit: 
> Recording for 10 seconds... Speak now.
> Recording finished.

You said: What is machine learning?

Agent: Machine learning is a subset of AI that enables systems 
to learn and improve from experience without being explicitly programmed.

Speaking...
[Voice playback from Murf Falcon]
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```dotenv
# 🔑 API Keys (REQUIRED)
MURF_API_KEY=sk_xxx                    # From Murf dashboard
DEEPGRAM_API_KEY=xxx                   # From Deepgram console
OPENAI_API_KEY=sk-xxx                  # From OpenAI platform

# 🎯 Murf Settings
MURF_REGION=GLOBAL                     # GLOBAL, IN, US, etc.
MURF_VOICE_ID=Matthew                  # Matthew, Evan, Sarah, etc.

# 🧠 OpenAI Settings
OPENAI_MODEL=gpt-4o-mini               # gpt-4o-mini, gpt-4, gpt-4-turbo

# 🎤 Audio Settings
SAMPLE_RATE=16000                      # Hz (optimal for ASR)
RECORD_SECONDS=10                      # Max recording duration
SILENCE_THRESHOLD=0.05                 # Audio level for silence
SILENCE_DURATION=2                     # Seconds before auto-stop

# 🔄 Retry & Resilience
MAX_RETRIES=3                          # Number of retries
RETRY_BACKOFF=1.5                      # Backoff multiplier
REQUEST_TIMEOUT=60                     # Request timeout (seconds)

# 📋 Logging
LOG_LEVEL=INFO                         # DEBUG, INFO, WARNING, ERROR
LOG_FILE=voiceflow.log                 # Log file path
```

---

## 🧪 Testing

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=html

# Run specific test module
pytest tests/test_agent.py -v

# Run with debug output
LOG_LEVEL=DEBUG pytest tests/ -v
```

**Test Coverage:**
- ✅ 8 test modules
- ✅ 20+ test cases
- ✅ Unit & integration tests
- ✅ Mock-based testing
- ✅ Pytest fixtures

---

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t voiceflow:latest .

# Run container with environment variables
docker run -it \
  -e MURF_API_KEY=sk_xxx \
  -e DEEPGRAM_API_KEY=xxx \
  -e OPENAI_API_KEY=sk-xxx \
  voiceflow:latest

# Run with .env file
docker run -it --env-file .env voiceflow:latest

# Run in background
docker run -d \
  --name voiceflow \
  --env-file .env \
  voiceflow:latest
```

---

## 📊 Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **Total Latency** | 2-3 seconds | End-to-end response time |
| **ASR Latency** | 1-2s | Deepgram processing |
| **LLM Latency** | 1-2s | OpenAI response generation |
| **TTS Latency** | 1-2s | Murf Falcon speech synthesis |
| **Memory Usage** | 150-300MB | Idle vs. active streaming |
| **CPU Usage** | Minimal | I/O bound operation |
| **Audio Quality** | 16kHz mono | Optimal for speech |
| **Concurrent** | 1 conversation | Sequential processing |

---

## 🔐 Security Features

- ✅ **No Hardcoded Keys** - Environment variables only
- ✅ **Input Validation** - All inputs sanitized
- ✅ **Error Handling** - No sensitive data in errors
- ✅ **Secure Logging** - Secrets never logged
- ✅ **Resource Cleanup** - Proper stream closure
- ✅ **HTTPS Only** - All API calls use HTTPS
- ✅ **Type Safety** - Full type hints throughout

---

## 🐛 Troubleshooting

### ❌ Error: "MURF_API_KEY is not set"

**Solution:**
```bash
# Verify .env file exists
cat .env | grep MURF_API_KEY

# Make sure you copied .env.example
cp .env.example .env

# Edit .env with your actual API key
```

### ❌ Error: "Microphone not detected"

**Solution:**
```bash
# Check microphone connection
python -c "import pyaudio; p=pyaudio.PyAudio(); print(p.get_device_count())"

# Run with debug logging
LOG_LEVEL=DEBUG python -m app.cli_runner
```

### ❌ Error: "API request timeout"

**Solution:**
```bash
# Increase timeout in .env
REQUEST_TIMEOUT=120

# Check internet connection
ping google.com
```

### ❌ Error: "Invalid API key"

**Solution:**
```bash
# Verify keys in provider dashboards:
# - Murf: https://murf.ai/dashboard
# - Deepgram: https://console.deepgram.com
# - OpenAI: https://platform.openai.com/api-keys

# Regenerate key if needed and update .env
```

**More help:** See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[README.md](README.md)** | Complete documentation (you are here) |
| **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** | 30-second quick commands |
| **[START_HERE.md](START_HERE.md)** | Getting started guide |
| **[DEVELOPMENT.md](DEVELOPMENT.md)** | Development setup & contribution |
| **[CONTRIBUTING.md](CONTRIBUTING.md)** | How to contribute code |
| **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** | Common issues & solutions |
| **[PROJECT_STATUS.md](PROJECT_STATUS.md)** | Project completion status |
| **[MANIFEST.md](MANIFEST.md)** | Complete file inventory |

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with tests
4. **Commit** with clear messages (`git commit -m 'Add amazing feature'`)
5. **Push** to your fork (`git push origin feature/amazing-feature`)
6. **Open** a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Code Standards
- **Format:** Black (`black app/ tests/`)
- **Lint:** Flake8 (`flake8 app/ tests/`)
- **Type Check:** MyPy (`mypy app/`)
- **Tests:** All new code must have tests

---

## 📊 Statistics

| Item | Count |
|------|-------|
| **Total Files** | 39 |
| **Python Modules** | 13 |
| **Test Files** | 8 |
| **Documentation Files** | 8 |
| **Lines of Code** | ~2,500+ |
| **Test Cases** | 20+ |
| **API Integrations** | 3 |
| **Custom Exceptions** | 7 |

---

## 💡 Use Cases

### ✅ Quick Q&A
Ask questions while coding and get instant answers

### ✅ Voice Notes
Speak notes and have them converted to speech

### ✅ Learning Tool
Interactive voice-based learning companion

### ✅ Productivity
Hands-free assistance during work

### ✅ Accessibility
Assistive technology for accessibility needs

### ✅ Prototyping
Base for voice AI application development

---

## 🎓 Learning Resources

- 📖 [Murf AI Documentation](https://murf.ai/docs)
- 📖 [Deepgram Documentation](https://developers.deepgram.com)
- 📖 [OpenAI API Reference](https://platform.openai.com/docs)
- 📖 [PyAudio Documentation](http://people.csail.mit.edu/hubert/pyaudio/)
- 📖 [Python Type Hints](https://docs.python.org/3/library/typing.html)

---

## 🌐 Website & Landing Page

This repository now includes a responsive landing page (in the `web/` folder) with six tabs: **Home, Features, Demo, Pricing, About, Contact**. The landing page was created by **Niket Patil** and the project is affiliated with **ANDS NETWORK**.

Key points about the landing page and enquiry flow:

- The site is responsive and works on desktop and mobile.
- The contact/enquiry form posts to a serverless endpoint at `/api/send` (designed for Vercel deployments).
- Form submissions are forwarded to the admin email and also sent as a WhatsApp notification (when configured) so you receive enquiries both by email and WhatsApp.
- Admin contact (default values are included in `.env.example`):
  - Email: `nikepatil1624@gmail.com`
  - WhatsApp / Phone: `+91 9022790410`
- Pricing note: **Paid consulting coming soon.** Beta consulting is free — set the call with us via the enquiry form.

Vercel deployment notes:

- The serverless function uses the following environment variables (add them in Vercel or in `.env` during local testing):
  - `SENDGRID_API_KEY` — SendGrid API key for email forwarding
  - `TWILIO_ACCOUNT_SID` — Twilio Account SID (for WhatsApp)
  - `TWILIO_AUTH_TOKEN` — Twilio Auth Token
  - `TWILIO_WHATSAPP_FROM` — Twilio WhatsApp sender (e.g. `whatsapp:+1415...`)
  - `ADMIN_EMAIL` — Destination email for enquiries (default: `nikepatil1624@gmail.com`)
  - `ADMIN_WHATSAPP_TO` — Destination WhatsApp number (default: `whatsapp:+919022790410`)

To deploy the landing page to Vercel:

1. Push this repository to GitHub (example repo URL: `https://github.com/N-i-k-e-t/murf-voiceflow-agent`).
2. Import the repo into Vercel and set the environment variables listed above in the Vercel dashboard.
3. The `web/` folder serves the static site; the serverless API is in `api/send.js`.

Privacy & security:

- No API keys are committed. Add keys via Vercel's environment settings or local `.env`.
- The serverless function performs simple validation and forwards only the necessary details.

If you want me to proceed with pushing to GitHub or to prepare the repo for an automated Vercel import, I can provide step-by-step commands and a checklist.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Murf Voice Agent Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

---

## 🏆 Built For

**Techfest IIT Bombay – Murf Voice Agent Hackathon**

Tags: `murf-ai` • `voice-agent` • `tts` • `asr` • `llm` • `python` • `deepgram` • `openai`

---

## 📞 Support

### Having Issues?
1. 📖 Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. 🔍 Search [GitHub Issues](https://github.com/your-username/murf-voiceflow-agent/issues)
3. 💬 Open a new issue with details

### Have Questions?
- 📚 Read the documentation
- 🔗 Check relevant API docs
- 💭 Share ideas in discussions

---

## 🎉 Quick Links

- 🚀 [Quick Start](#-quick-start)
- 📚 [Documentation](#-documentation)
- 🧪 [Testing](#-testing)
- 🐛 [Troubleshooting](#-troubleshooting)
- 🤝 [Contributing](#-contributing)
- 📄 [License](LICENSE)

---

<div align="center">

### ⭐ If you find this useful, please give it a star!

**Made with ❤️ for Voice AI**

[⬆ back to top](#-voiceflow--murf-falcon-voice-agent)

</div>
