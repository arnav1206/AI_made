"""
utils/speech_to_text.py
========================
Speech-to-Text module for Bharat Voice2Form.

Features:
- Converts WebM, OGG, MP3, WAV audio from browser microphone into 16kHz Mono PCM WAV.
- Safe audio volume normalization with peak clipping.
- OpenAI Whisper local STT support & SpeechRecognition API.
- Safe fallback & mock transcripts for 9 Indian languages.
"""

from __future__ import annotations

import io
import os
import subprocess
import logging
import imageio_ffmpeg
import wave

from utils.constants import MOCK_TRANSCRIPTS, LANGUAGES

logger = logging.getLogger(__name__)

# ─── Config ────────────────────────────────────────────────────────
ENGINE: str = "google_free"

_LOCALE_MAP: dict[str, str] = {
    lang[1]: lang[3] for lang in LANGUAGES
}
_LOCALE_MAP["English"] = "en-IN"


class TranscriptionResult:
    """Structured return value from transcribe()."""

    def __init__(self, text: str, language: str, confidence: float, engine: str):
        self.text       = text
        self.language   = language
        self.confidence = confidence
        self.engine     = engine
        self.error: str | None = None

    def __bool__(self) -> bool:
        return bool(self.text) and self.error is None


def convert_audio_to_pcm_wav(audio_bytes: bytes) -> bytes:
    """
    Convert raw audio bytes to 16kHz 16-bit Mono PCM WAV bytes.
    """
    try:
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        cmd = [
            ffmpeg_exe,
            "-hide_banner",
            "-loglevel", "error",
            "-i", "pipe:0",
            "-f", "wav",
            "-acodec", "pcm_s16le",
            "-ac", "1",
            "-ar", "16000",
            "-y",
            "pipe:1",
        ]
        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        out, err = proc.communicate(input=audio_bytes)
        if proc.returncode == 0 and len(out) > 44:
            return boost_audio_volume(out)
        else:
            logger.warning("FFmpeg conversion error: %s", err.decode("utf-8", errors="ignore"))
    except Exception as exc:
        logger.warning("FFmpeg audio conversion error: %s", exc)

    return audio_bytes


def boost_audio_volume(wav_bytes: bytes, target_peak: float = 24000.0) -> bytes:
    """
    Safely boost audio volume without integer overflow.
    """
    try:
        import audioop
        f = io.BytesIO(wav_bytes)
        with wave.open(f, "rb") as w:
            params = w.getparams()
            raw_frames = w.readframes(w.getnframes())

        if not raw_frames:
            return wav_bytes

        max_val = audioop.max(raw_frames, 2)
        if 0 < max_val < target_peak:
            factor = min(target_peak / float(max_val), 10.0)
            raw_frames = audioop.mul(raw_frames, 2, min(factor, 8.0))

        out_buf = io.BytesIO()
        with wave.open(out_buf, "wb") as out_w:
            out_w.setparams(params)
            out_w.writeframes(raw_frames)
        return out_buf.getvalue()
    except Exception as exc:
        logger.warning("Volume boost error: %s", exc)
        return wav_bytes


def transcribe(
    audio_bytes: bytes | None = None,
    language: str = "Hindi",
    *,
    engine: str | None = None,
) -> TranscriptionResult:
    """
    Transcribe audio bytes to text in the specified language.
    """
    selected_engine = engine or ENGINE

    if audio_bytes is None:
        return _transcribe_mock(language)

    try:
        if selected_engine == "whisper":
            return _transcribe_whisper(audio_bytes, language)
        else:
            return _transcribe_google_free(audio_bytes, language)
    except Exception as exc:
        logger.warning("STT transcription failed: %s", exc)
        result = _transcribe_mock(language)
        result.error = str(exc)
        return result


def _transcribe_whisper(audio_bytes: bytes, language: str) -> TranscriptionResult:
    """OpenAI Whisper STT engine."""
    import whisper, tempfile
    wav_bytes = convert_audio_to_pcm_wav(audio_bytes)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        f.write(wav_bytes)
        tmp_path = f.name

    try:
        model = whisper.load_model("tiny")
        res = model.transcribe(tmp_path)
        os.unlink(tmp_path)
        return TranscriptionResult(res["text"].strip(), language, 0.95, "OpenAI Whisper")
    except Exception as e:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise e


def get_supported_languages() -> list[str]:
    if isinstance(MOCK_TRANSCRIPTS, dict):
        return list(MOCK_TRANSCRIPTS.keys())
    return ["Hindi", "English", "Odia", "Tamil", "Telugu", "Bengali", "Marathi", "Kannada", "Malayalam"]


def _transcribe_mock(language: str) -> TranscriptionResult:
    if isinstance(MOCK_TRANSCRIPTS, dict):
        text = MOCK_TRANSCRIPTS.get(language, MOCK_TRANSCRIPTS.get("English", ""))
    elif isinstance(MOCK_TRANSCRIPTS, (list, tuple)) and MOCK_TRANSCRIPTS:
        text = str(MOCK_TRANSCRIPTS[0])
    else:
        text = (
            "मेरा नाम राहुल शर्मा है। मैं जयपुर राजस्थान का रहने वाला हूँ। "
            "मैं B.Tech द्वितीय वर्ष का छात्र हूँ और बीआईटी संस्थान में पढ़ता हूँ। "
            "मेरी जन्मतिथि 15/08/2003 है और मेरी परिवार की वार्षिक आय ₹1,50,000 है। "
            "मेरा फोन नंबर 9876543210 और ईमेल rahul.sharma@example.com है।"
        )

    return TranscriptionResult(
        text=text,
        language=language,
        confidence=1.0,
        engine="mock",
    )


def _transcribe_google_free(audio_bytes: bytes, language: str) -> TranscriptionResult:
    import speech_recognition as sr

    wav_bytes = convert_audio_to_pcm_wav(audio_bytes)
    locale = _LOCALE_MAP.get(language, "hi-IN")
    r = sr.Recognizer()

    audio_file = io.BytesIO(wav_bytes)
    with sr.AudioFile(audio_file) as source:
        r.adjust_for_ambient_noise(source, duration=0.1)
        audio_data = r.record(source)

    try:
        text = r.recognize_google(audio_data, language=locale)
        if text.strip():
            return TranscriptionResult(text, language, 0.95, "Google Speech API")
    except sr.UnknownValueError:
        pass
    except sr.RequestError as req_err:
        logger.warning("Google Speech API request error: %s", req_err)

    fallbacks = ["hi-IN", "en-IN"] if locale != "en-IN" else ["hi-IN"]
    for fb_locale in fallbacks:
        try:
            audio_file.seek(0)
            with sr.AudioFile(audio_file) as source:
                audio_data = r.record(source)
            fb_text = r.recognize_google(audio_data, language=fb_locale)
            if fb_text.strip():
                return TranscriptionResult(fb_text, language, 0.88, "Google Speech API")
        except Exception:
            continue

    res = TranscriptionResult("", language, 0.0, "Google Speech API")
    res.error = "Could not understand speech. Please speak into the mic or type details."
    return res
