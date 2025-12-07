"""Audio utilities for recording and playback."""

import io
import wave
import logging
from typing import Optional

import pyaudio  # type: ignore

logger = logging.getLogger(__name__)


def record_audio(
    sample_rate: int = 16000,
    channels: int = 1,
    record_seconds: int = 5,
    silence_threshold: float = 0.05,
    silence_duration: int = 2,
) -> Optional[bytes]:
    """
    Record audio from microphone with auto-stop on silence.

    Args:
        sample_rate: Sample rate in Hz
        channels: Number of audio channels
        record_seconds: Maximum recording duration
        silence_threshold: Audio level threshold for silence detection
        silence_duration: Seconds of silence before stopping

    Returns:
        WAV audio bytes or None if recording failed
    """
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=channels,
            rate=sample_rate,
            input=True,
            frames_per_buffer=1024,
        )

        logger.info(f"Recording for up to {record_seconds} seconds...")
        frames = []
        total_frames = int(sample_rate / 1024 * record_seconds)
        silence_frames = int(sample_rate / 1024 * silence_duration)
        silent_count = 0

        for i in range(total_frames):
            try:
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)

                # Simple silence detection
                audio_level = max(abs(int.from_bytes(data[j : j + 2], "little", signed=True))
                                   for j in range(0, len(data), 2))

                if audio_level < silence_threshold * 32768:
                    silent_count += 1
                    if silent_count > silence_frames:
                        logger.info("Silence detected, stopping recording.")
                        break
                else:
                    silent_count = 0

            except Exception as e:
                logger.warning(f"Error reading audio frame: {e}")
                continue

        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save to WAV in memory
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(sample_rate)
            wf.writeframes(b"".join(frames))

        logger.info(f"Recording complete ({len(frames)} frames)")
        return buffer.getvalue()

    except Exception as e:
        logger.error(f"Recording failed: {e}")
        return None


def play_audio_stream(audio_chunks, sample_rate: int = 24000) -> bool:
    """
    Play PCM audio chunks from stream.

    Args:
        audio_chunks: Iterator/list of audio byte chunks
        sample_rate: Sample rate in Hz

    Returns:
        True if playback completed successfully
    """
    try:
        audio = pyaudio.PyAudio()
        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            output=True,
        )

        logger.info("Starting audio playback...")
        chunk_count = 0

        try:
            for chunk in audio_chunks:
                if chunk:
                    stream.write(chunk)
                    chunk_count += 1
        finally:
            stream.stop_stream()
            stream.close()
            audio.terminate()

        logger.info(f"Playback complete ({chunk_count} chunks)")
        return True

    except Exception as e:
        logger.error(f"Playback failed: {e}")
        return False
