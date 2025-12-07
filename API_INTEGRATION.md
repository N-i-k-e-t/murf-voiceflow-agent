# 🔌 API Integration Guide with Visuals

## 📊 API Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        VoiceFlow APIs                               │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌───────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │  🎯 Deepgram      │  │  🧠 OpenAI       │  │  🔊 Murf Falcon  │  │
│  ├───────────────────┤  ├──────────────────┤  ├──────────────────┤  │
│  │ Speech-to-Text    │  │ Language Model   │  │ Text-to-Speech   │  │
│  │ (ASR)             │  │ (LLM)            │  │ (TTS)            │  │
│  │                   │  │                  │  │                  │  │
│  │ ✅ Real-time      │  │ ✅ Multi-turn    │  │ ✅ Streaming     │  │
│  │ ✅ Nova-3 Model   │  │ ✅ Context aware │  │ ✅ Natural voice │  │
│  │ ✅ Smart format   │  │ ✅ 20+ languages │  │ ✅ 40+ voices    │  │
│  │                   │  │                  │  │                  │  │
│  │ 🔗 REST API       │  │ 🔗 REST API      │  │ 🔗 REST API      │  │
│  │ 🔐 Token auth     │  │ 🔐 Key auth      │  │ 🔐 Key auth      │  │
│  └───────────────────┘  └──────────────────┘  └──────────────────┘  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 1. 🎯 Deepgram API (Speech-to-Text)

### Endpoint Diagram

```
User Audio (WAV)
       │
       ▼
┌──────────────────────────────────────┐
│  POST /v1/listen                     │
│  https://api.deepgram.com/v1/listen  │
├──────────────────────────────────────┤
│                                      │
│  Headers:                            │
│  ├─ Authorization: Token {KEY}       │
│  └─ Content-Type: audio/wav          │
│                                      │
│  Query Params:                       │
│  ├─ model=nova-3                     │
│  ├─ smart_format=true                │
│  └─ language=en                      │
│                                      │
│  Body:                               │
│  └─ [Binary WAV audio data]          │
│                                      │
└──────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────┐
│  Response (200 OK)                   │
├──────────────────────────────────────┤
│                                      │
│  {                                   │
│    "results": {                      │
│      "channels": [{                  │
│        "alternatives": [{            │
│          "transcript": "What is...",  │
│          "confidence": 0.95           │
│        }]                            │
│      }]                              │
│    }                                 │
│  }                                   │
│                                      │
└──────────────────────────────────────┘
       │
       ▼
Text Transcript
```

### Implementation in VoiceFlow

```python
# app/asr_deepgram.py

class DeepgramASRClient:
    def __init__(self):
        self.base_url = "https://api.deepgram.com/v1/listen"
        self.session = requests.Session()
        # Retry strategy with backoff
        
    def transcribe_wav(self, wav_bytes: bytes) -> Optional[str]:
        headers = {
            "Authorization": f"Token {DEEPGRAM_API_KEY}",
            "Content-Type": "audio/wav"
        }
        params = {
            "model": "nova-3",        # Latest accurate model
            "smart_format": "true",    # Enable punctuation
        }
        response = self.session.post(
            self.base_url,
            headers=headers,
            params=params,
            data=wav_bytes,
            timeout=REQUEST_TIMEOUT
        )
        # Extract transcript from response
        return response.json()["results"]["channels"][0]["alternatives"][0]["transcript"]
```

### Configuration

```dotenv
DEEPGRAM_API_KEY=your_deepgram_api_key_here
```

---

## 2. 🧠 OpenAI API (Language Model)

### Endpoint Diagram

```
Transcript Text + Context
       │
       ▼
┌──────────────────────────────────────────┐
│  POST /v1/chat/completions               │
│  https://api.openai.com/v1/chat/completions
├──────────────────────────────────────────┤
│                                          │
│  Headers:                                │
│  ├─ Authorization: Bearer {KEY}          │
│  ├─ Content-Type: application/json       │
│  └─ User-Agent: voiceflow/1.0            │
│                                          │
│  Body (JSON):                            │
│  {                                       │
│    "model": "gpt-4o-mini",               │
│    "messages": [                         │
│      {                                   │
│        "role": "system",                 │
│        "content": "You are VoiceFlow..." │
│      },                                  │
│      {                                   │
│        "role": "user",                   │
│        "content": "What is AI?"          │
│      }                                   │
│    ],                                    │
│    "temperature": 0.7,                   │
│    "max_tokens": 500                     │
│  }                                       │
│                                          │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Response (200 OK)                       │
├──────────────────────────────────────────┤
│                                          │
│  {                                       │
│    "id": "chatcmpl-xxx",                │
│    "object": "chat.completion",         │
│    "choices": [{                        │
│      "message": {                       │
│        "role": "assistant",             │
│        "content": "AI is a technology..."
│      },                                 │
│      "finish_reason": "stop"            │
│    }],                                  │
│    "usage": {                           │
│      "prompt_tokens": 50,               │
│      "completion_tokens": 150,          │
│      "total_tokens": 200                │
│    }                                    │
│  }                                      │
│                                          │
└──────────────────────────────────────────┘
       │
       ▼
Response Text
```

### Implementation in VoiceFlow

```python
# app/llm_openai.py

from openai import OpenAI

class LLMClient:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def chat(self, messages: List[Dict[str, str]]) -> str:
        completion = self.client.chat.completions.create(
            model=OPENAI_MODEL,  # gpt-4o-mini
            messages=messages,    # [system, user, assistant, ...]
            temperature=0.7,      # Balanced creativity
            max_tokens=500        # Response length
        )
        return completion.choices[0].message.content.strip()
```

### Multi-Turn Conversation Example

```
Turn 1:
User:   "What is machine learning?"
Assistant: "Machine learning is..."

Turn 2:
User:   "Can you explain neural networks?"
Assistant: "Neural networks are inspired by..."
(Context from Turn 1 is maintained!)

Turn 3:
User:   "How does backpropagation work?"
Assistant: "Backpropagation is used to train..."
(Full context history is maintained!)
```

### Configuration

```dotenv
OPENAI_API_KEY=sk_your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini  # gpt-4o, gpt-4-turbo, etc.
```

---

## 3. 🔊 Murf Falcon API (Text-to-Speech)

### Endpoint Diagram

```
Response Text
       │
       ▼
┌──────────────────────────────────────────┐
│  POST /v1/speech/synthesize              │
│  (via Murf Python SDK)                   │
├──────────────────────────────────────────┤
│                                          │
│  Parameters:                             │
│  ├─ text: "Your response text"          │
│  ├─ voice_id: "Matthew"                 │
│  ├─ model: "FALCON"                     │
│  ├─ sample_rate: 24000                  │
│  ├─ format: "PCM"                       │
│  └─ region: "GLOBAL"                    │
│                                          │
│  Returns:                                │
│  └─ Iterator of audio chunks (Streaming)
│                                          │
└──────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────┐
│  Audio Stream (Real-time)                │
├──────────────────────────────────────────┤
│                                          │
│  Chunk 1: [PCM data - 4KB]              │
│  Chunk 2: [PCM data - 4KB]              │
│  Chunk 3: [PCM data - 4KB]              │
│  ...                                     │
│  Chunk N: [PCM data - remaining]        │
│                                          │
│  Total: 24kHz, mono, 16-bit PCM         │
│                                          │
└──────────────────────────────────────────┘
       │
       ▼
Audio Playback (Live Streaming!)
```

### Implementation in VoiceFlow

```python
# app/tts_murf.py

from murf import Murf, MurfRegion

class MurfTTSClient:
    def __init__(self):
        region = getattr(MurfRegion, MURF_REGION, MurfRegion.GLOBAL)
        self.client = Murf(api_key=MURF_API_KEY, region=region)
        
    def stream_tts(self, text: str) -> Iterable[bytes]:
        # Real-time streaming
        audio_stream = self.client.text_to_speech.stream(
            text=text,
            voice_id=MURF_VOICE_ID,        # "Matthew"
            model="FALCON",                 # Latest model
            sample_rate=24000,              # Hz
            format="PCM",                   # 16-bit PCM
            multi_native_locale="en-US"    # English
        )
        return audio_stream  # Iterator of bytes chunks
```

### Available Voices

```
Murf Falcon Voices:
├─ Matthew (Male, Professional)
├─ Evan (Male, Friendly)
├─ Sarah (Female, Clear)
├─ Emma (Female, Warm)
├─ James (Male, Deep)
├─ Lisa (Female, Energetic)
└─ ... (40+ voices available)
```

### Configuration

```dotenv
MURF_API_KEY=your_murf_api_key_here
MURF_REGION=GLOBAL          # GLOBAL, IN, US
MURF_VOICE_ID=Matthew       # Any Murf voice
```

---

## 🔄 Complete API Flow with Timing

```
Time: 00:00 ┬─ User presses Enter
            │
Time: 00:01 │ Recording starts (audio input)
            │
Time: 00:10 │ Recording ends
            │
            ├─ WAV data ready (10 seconds of audio ≈ 320KB)
            │
Time: 00:11 │ Deepgram ASR Request
            │ ├─ Network latency: ~200ms
            │ ├─ API processing: ~1-2s
            │ └─ Network latency: ~200ms
            │
Time: 00:13 │ Transcript received: "What is machine learning?"
            │
Time: 00:14 │ OpenAI LLM Request
            │ ├─ Network latency: ~100ms
            │ ├─ API processing: ~1-2s
            │ └─ Network latency: ~100ms
            │
Time: 00:16 │ Response received: "Machine learning is a subset of AI..."
            │
Time: 00:17 │ Murf Falcon TTS Request (Streaming)
            │ ├─ Network latency: ~100ms
            │ └─ Streaming audio chunks (~2s)
            │
Time: 00:19 │ Audio playback starts (streaming in real-time)
            │
Time: 00:22 │ Audio playback ends
            │
            └─ Total latency: 22 seconds (~2-3s API latency + 10s recording + 10s playback)
```

---

## 🛡️ Error Handling for APIs

```
┌─────────────────────────────────┐
│  API Call                       │
└────────────┬────────────────────┘
             │
             ▼
    ┌────────────────┐
    │  Success?      │
    └────┬──────┬───┘
         │      │
       Yes │   No│
         │      │
         │      ▼
         │   ┌─────────────────────┐
         │   │  HTTP Status Code   │
         │   └────┬────┬────┬─────┘
         │        │    │    │
         │      400 429  500  ???
         │        │    │    │
         │        ▼    ▼    ▼
         │     Invalid Too  Server
         │     Request Rate Error
         │        │    │    │
         │        │    ▼    ▼
         │        │  Retry  Retry
         │        │  (Backoff)
         │        │    │    │
         │        ▼    ▼    ▼
         │     Log & Notify User
         │        │
         └────────┴─────────────→ Continue/Fail
```

---

## 📝 API Key Setup Steps

### 1. Deepgram

```
1. Go to https://console.deepgram.com
2. Sign up / Login
3. Create new API key
4. Copy the key
5. Add to .env:
   DEEPGRAM_API_KEY=<paste-key-here>
```

### 2. OpenAI

```
1. Go to https://platform.openai.com/api-keys
2. Sign up / Login
3. Create new secret key
4. Copy the key (only shown once!)
5. Add to .env:
   OPENAI_API_KEY=<paste-key-here>
```

### 3. Murf Falcon

```
1. Go to https://murf.ai/dashboard
2. Sign up / Login
3. Create new API key
4. Copy the key
5. Add to .env:
   MURF_API_KEY=<paste-key-here>
```

---

## 🔍 API Response Times (Benchmarks)

| Operation | Time | Range |
|-----------|------|-------|
| Deepgram ASR | 1-2s | Depends on audio length |
| OpenAI LLM | 1-2s | Depends on response length |
| Murf TTS | 1-2s | Depends on text length |
| Network (total) | ~400ms | Per API call |
| **Total Pipeline** | **2-3s** | User to Response |

---

## 🚀 Rate Limits

| API | Free Tier | Paid Tier |
|-----|-----------|-----------|
| **Deepgram** | 50,000 min/mo | Pay per usage |
| **OpenAI** | $5 credit | $20+/mo |
| **Murf Falcon** | Limited | Pay per usage |

---

This guide provides complete visual reference for all API integrations!
