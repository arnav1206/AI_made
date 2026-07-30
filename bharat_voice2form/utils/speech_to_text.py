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
ENGINE: str = "groq_whisper"     # Primary: Groq Whisper Large V3 Turbo (falls back to wispr_flow / google_free)

_LOCALE_MAP: dict[str, str] = {
    lang[1]: lang[3] for lang in LANGUAGES
}
_LOCALE_MAP["English"] = "en-IN"


def _detect_audio_extension(audio_bytes: bytes) -> str:
    """Detect audio file extension (.webm, .ogg, .wav, .mp3, .m4a) from header magic bytes."""
    if not audio_bytes or len(audio_bytes) < 4:
        return ".webm"
    if audio_bytes.startswith(b"\x1a\x45\xdf\xa3"):
        return ".webm"
    if audio_bytes.startswith(b"OggS"):
        return ".ogg"
    if audio_bytes.startswith(b"RIFF") and b"WAVE" in audio_bytes[:16]:
        return ".wav"
    if audio_bytes.startswith(b"ID3") or audio_bytes.startswith(b"\xff\xfb"):
        return ".mp3"
    return ".webm"


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
        if selected_engine in ("groq_whisper", "wispr_flow"):
            return _transcribe_groq_whisper(audio_bytes, language)
        elif selected_engine == "whisper":
            return _transcribe_whisper(audio_bytes, language)
        else:
            return _transcribe_google_free(audio_bytes, language)
    except Exception as exc:
        logger.warning("STT transcription failed: %s", exc)
        result = _transcribe_mock(language)
        result.error = str(exc)
        return result


def _transcribe_whisper(audio_bytes: bytes, language: str) -> TranscriptionResult:
    """OpenAI Whisper STT engine (local via whisper library)."""
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


def _transcribe_groq_whisper(audio_bytes: bytes, language: str) -> TranscriptionResult:
    """
    Groq Whisper Large V3 Turbo STT engine.
    Ultra-fast (216x real-time), production-grade, multilingual Indian language support.
    Requires GROQ_API_KEY in Streamlit secrets or environment variable.
    Falls back to Google Free STT if key is not configured.
    """
    import os, io, tempfile
    import streamlit as st

    # Resolve Groq API key
    groq_api_key = (
        st.secrets.get("GROQ_API_KEY")
        if hasattr(st, "secrets")
        else os.environ.get("GROQ_API_KEY", "")
    )
    if not groq_api_key:
        logger.info("GROQ_API_KEY not set — falling back to Google Free STT")
        return _transcribe_google_free(audio_bytes, language)

    from groq import Groq

    locale = _LOCALE_MAP.get(language, "hi")
    language_code = locale.split("-")[0]   # e.g. "hi" from "hi-IN"

    ext = _detect_audio_extension(audio_bytes)
    filename = f"audio{ext}"

    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        client = Groq(api_key=groq_api_key)
        with open(tmp_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                model="whisper-large-v3-turbo",
                language=language_code,
                response_format="text",
                prompt=f"Indian government form application voice dictation in {language}.",
            )
        text = str(transcription).strip()
        if text:
            return TranscriptionResult(text, language, 0.98, "Groq Whisper Large V3 Turbo")
        else:
            raise ValueError("Empty transcription from Groq Whisper")
    except Exception as exc:
        logger.warning("Groq Whisper failed on raw audio (%s): %s — trying PCM WAV fallback", ext, exc)
        try:
            wav_bytes = convert_audio_to_pcm_wav(audio_bytes)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav:
                tmp_wav.write(wav_bytes)
                tmp_wav_path = tmp_wav.name
            with open(tmp_wav_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    file=("audio.wav", audio_file.read()),
                    model="whisper-large-v3-turbo",
                    language=language_code,
                    response_format="text",
                )
            if os.path.exists(tmp_wav_path):
                os.unlink(tmp_wav_path)
            text = str(transcription).strip()
            if text:
                return TranscriptionResult(text, language, 0.98, "Groq Whisper Large V3 Turbo (PCM)")
        except Exception as exc2:
            logger.warning("FFmpeg Groq fallback failed: %s — falling back to Google Free STT", exc2)

        return _transcribe_google_free(audio_bytes, language)
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _transcribe_wispr_flow(audio_bytes: bytes, language: str) -> TranscriptionResult:
    """
    Wispr Flow Voice Interface REST API integration.
    Endpoint: https://platform-api.wisprflow.ai/api/v1/dash/api
    Requires WISPR_FLOW_API_KEY in Streamlit secrets or environment variable.
    Falls back to Groq Whisper if key is not configured.
    """
    import os, base64, urllib.request, json
    import streamlit as st

    # Resolve Wispr Flow API key
    wispr_key = (
        st.secrets.get("WISPR_FLOW_API_KEY")
        if hasattr(st, "secrets")
        else os.environ.get("WISPR_FLOW_API_KEY", "")
    )
    if not wispr_key:
        logger.info("WISPR_FLOW_API_KEY not configured — using Groq Whisper Large V3 Turbo")
        return _transcribe_groq_whisper(audio_bytes, language)

    try:
        wav_bytes = convert_audio_to_pcm_wav(audio_bytes)
        base64_audio = base64.b64encode(wav_bytes).decode("utf-8")

        payload = json.dumps({
            "audio": base64_audio,
            "language": _LOCALE_MAP.get(language, "hi-IN").split("-")[0],
            "context": {"app": "Bharat Voice2Form", "language": language}
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://platform-api.wisprflow.ai/api/v1/dash/api",
            data=payload,
            headers={
                "Authorization": f"Bearer {wispr_key}",
                "Content-Type": "application/json",
            },
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            text = data.get("text") or data.get("transcription") or ""
            if text:
                return TranscriptionResult(text.strip(), language, 0.98, "Wispr Flow AI")
            else:
                raise ValueError(f"Empty transcription response: {data}")

    except Exception as exc:
        logger.warning("Wispr Flow API failed: %s — falling back to Groq Whisper", exc)
        return _transcribe_groq_whisper(audio_bytes, language)


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
