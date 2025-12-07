import io
import logging
import sys
import wave
from typing import Optional

import pyaudio  # type: ignore
from colorama import Fore, Style, init as colorama_init  # type: ignore

from .config import SAMPLE_RATE, CHANNELS, RECORD_SECONDS, LOG_LEVEL
from .asr_deepgram import DeepgramASRClient
from .tts_murf import MurfTTSClient
from .agent import VoiceAgent

logger = logging.getLogger(__name__)

# Audio constants
CHUNK_SIZE = 1024
TTS_SAMPLE_RATE = 24000  # Murf Falcon default sample rate


def setup_logging(level: str = LOG_LEVEL) -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    logger.debug(f"Logging configured at level {level}")


def record_audio() -> Optional[bytes]:
    """
    Record audio from default microphone and return WAV bytes.
    
    Returns:
        WAV bytes or None if recording failed
    """
    audio = None
    stream = None
    
    try:
        audio = pyaudio.PyAudio()
        
        # List available devices (helpful for debugging)
        device_count = audio.get_device_count()
        logger.debug(f"Found {device_count} audio devices")
        
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
        )

        print(
            Fore.YELLOW
            + f"🎤 Recording for {RECORD_SECONDS} seconds... Speak now."
            + Style.RESET_ALL
        )
        
        frames = []
        num_chunks = int(SAMPLE_RATE / CHUNK_SIZE * RECORD_SECONDS)
        
        for i in range(num_chunks):
            try:
                data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
                frames.append(data)
            except Exception as e:
                logger.error(f"Error reading audio chunk {i}: {e}")
                continue

        print(Fore.YELLOW + "✓ Recording finished." + Style.RESET_ALL)

        if not frames:
            logger.warning("No audio frames recorded")
            return None

        # Save to WAV in memory
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b"".join(frames))

        wav_data = buffer.getvalue()
        logger.debug(f"Recorded {len(wav_data)} bytes of audio")
        return wav_data

    except OSError as e:
        logger.error(f"Audio device error: {e}. Check microphone connection.")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during recording: {e}")
        return None
    finally:
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except Exception as e:
                logger.warning(f"Error closing audio stream: {e}")
        if audio:
            try:
                audio.terminate()
            except Exception as e:
                logger.warning(f"Error terminating PyAudio: {e}")


def play_audio_stream(audio_chunks) -> bool:
    """
    Play PCM16 audio chunks from Murf streaming API.
    
    Args:
        audio_chunks: Iterator of audio chunk bytes
        
    Returns:
        True if playback successful, False otherwise
    """
    if not audio_chunks:
        logger.warning("No audio chunks to play")
        return False

    audio = None
    stream = None

    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=TTS_SAMPLE_RATE,
            output=True,
        )

        bytes_played = 0
        chunk_count = 0

        for chunk in audio_chunks:
            if chunk:
                try:
                    stream.write(chunk)
                    bytes_played += len(chunk)
                    chunk_count += 1
                except Exception as e:
                    logger.error(f"Error playing audio chunk {chunk_count}: {e}")
                    continue

        logger.debug(f"Playback complete: {chunk_count} chunks, {bytes_played} bytes")
        return True

    except OSError as e:
        logger.error(f"Audio playback device error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during playback: {e}")
        return False
    finally:
        if stream:
            try:
                stream.stop_stream()
                stream.close()
            except Exception as e:
                logger.warning(f"Error closing playback stream: {e}")
        if audio:
            try:
                audio.terminate()
            except Exception as e:
                logger.warning(f"Error terminating PyAudio: {e}")


def main() -> None:
    """Main CLI loop for VoiceFlow agent."""
    setup_logging()
    
    try:
        colorama_init(autoreset=True)
        
        # Initialize clients
        logger.info("Initializing VoiceFlow components...")
        asr = DeepgramASRClient()
        tts = MurfTTSClient()
        agent = VoiceAgent()

        print(
            Fore.CYAN
            + "╔════════════════════════════════════════════════════════╗\n"
            + "║  🎤 VoiceFlow – Murf Falcon Voice Agent (v1.0)         ║\n"
            + "║  Built for Techfest IIT Bombay – Murf Hackathon       ║\n"
            + "╚════════════════════════════════════════════════════════╝"
            + Style.RESET_ALL
        )
        print(Fore.YELLOW + "Commands:" + Style.RESET_ALL)
        print(f"  {Fore.GREEN}[Enter]{Style.RESET_ALL} to start recording your query")
        print(f"  {Fore.GREEN}'r'{Style.RESET_ALL} to reset conversation")
        print(f"  {Fore.GREEN}'q'{Style.RESET_ALL} to quit\n")

        conversation_count = 0
        
        while True:
            user_input = input(
                Fore.GREEN + "[Enter] to record, 'r' to reset, 'q' to quit: " + Style.RESET_ALL
            ).strip().lower()
            
            if user_input == "q":
                print(Fore.CYAN + "👋 Goodbye! Thanks for using VoiceFlow." + Style.RESET_ALL)
                break
            
            if user_input == "r":
                agent.reset_conversation()
                print(Fore.CYAN + "🔄 Conversation reset." + Style.RESET_ALL)
                continue
            
            if user_input != "":
                continue

            # Record audio
            print()
            wav_bytes = record_audio()
            if not wav_bytes:
                print(
                    Fore.RED
                    + "❌ Recording failed. Please check your microphone and try again."
                    + Style.RESET_ALL
                )
                continue

            # Transcribe
            print(Fore.YELLOW + "🔄 Transcribing..." + Style.RESET_ALL)
            transcript: Optional[str] = asr.transcribe_wav(wav_bytes)

            if not transcript:
                print(
                    Fore.RED
                    + "❌ ASR could not understand audio. Please speak clearly and try again."
                    + Style.RESET_ALL
                )
                continue

            print(Fore.MAGENTA + f"📝 You said: {transcript}" + Style.RESET_ALL)

            # Generate response
            print(Fore.YELLOW + "🤖 Generating response..." + Style.RESET_ALL)
            reply_text = agent.reply(transcript)
            
            if not reply_text:
                print(
                    Fore.RED
                    + "❌ Failed to generate response. Please try again."
                    + Style.RESET_ALL
                )
                continue

            print(Fore.BLUE + f"🗣️  Agent: {reply_text}" + Style.RESET_ALL)

            # Synthesize and play
            print(Fore.YELLOW + "🔊 Speaking..." + Style.RESET_ALL)
            audio_chunks = tts.stream_tts(reply_text)
            
            if audio_chunks:
                play_audio_stream(audio_chunks)
                conversation_count += 1
            else:
                print(Fore.RED + "❌ TTS failed. Could not generate speech." + Style.RESET_ALL)
            
            print()

    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n⚠️  Interrupted by user." + Style.RESET_ALL)
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error in main loop: {e}", exc_info=True)
        print(
            Fore.RED
            + f"❌ Fatal error: {e}\nPlease check the logs for details."
            + Style.RESET_ALL
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
