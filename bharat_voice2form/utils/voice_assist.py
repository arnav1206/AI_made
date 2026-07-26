"""
utils/voice_assist.py
======================
Voice Assistant module for Formitra.

Features:
- Converts text into spoken audio in 9 Indian languages using gTTS / Web Speech.
- Provides HTML5 browser speech synthesizer and Streamlit audio generator.
- Reads out form instructions, field status, missing required fields, and auto-fill summary.
"""

from __future__ import annotations

import io
import logging
import streamlit as st

logger = logging.getLogger(__name__)

# Map app languages to gTTS language codes
_GTTS_LANG_CODES: dict[str, str] = {
    "Hindi":     "hi",
    "Odia":      "or",
    "Tamil":     "ta",
    "Telugu":    "te",
    "Bengali":   "bn",
    "Marathi":   "mr",
    "Kannada":   "kn",
    "Malayalam": "ml",
    "English":   "en",
}

# Map app languages to HTML5 SpeechSynthesis locales
_WEB_TTS_LOCALES: dict[str, str] = {
    "Hindi":     "hi-IN",
    "Odia":      "or-IN",
    "Tamil":     "ta-IN",
    "Telugu":    "te-IN",
    "Bengali":   "bn-IN",
    "Marathi":   "mr-IN",
    "Kannada":   "kn-IN",
    "Malayalam": "ml-IN",
    "English":   "en-IN",
}


def generate_tts_audio_bytes(text: str, language: str = "Hindi") -> bytes | None:
    """
    Generate MP3 audio bytes for text in target Indian language using gTTS.
    """
    if not text or not text.strip():
        return None

    try:
        from gtts import gTTS
        lang_code = _GTTS_LANG_CODES.get(language, "hi")
        tts = gTTS(text=text.strip(), lang=lang_code, slow=False)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return fp.read()
    except Exception as exc:
        logger.warning("gTTS audio generation error for lang '%s': %s", language, exc)
        return None


def render_voice_assistant_player(text: str, language: str = "Hindi", label: str = "🔊 Listen to Voice Assist"):
    """
    Renders an interactive Voice Assistant button with browser speech synthesis.
    """
    locale = _WEB_TTS_LOCALES.get(language, "hi-IN")
    clean_text = text.replace("'", "\\'").replace("\n", " ")

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: 'Inter', system-ui, sans-serif;
                margin: 0;
                padding: 4px;
                background: transparent;
            }}
            .tts-btn {{
                background: linear-gradient(135deg, #1E40AF 0%, #1D4ED8 100%);
                color: #FFFFFF;
                border: none;
                border-radius: 50px;
                padding: 0.65rem 1.4rem;
                font-size: 0.92rem;
                font-weight: 700;
                cursor: pointer;
                box-shadow: 0 4px 14px rgba(30, 64, 175, 0.3);
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 0.5rem;
            }}
            .tts-btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 6px 18px rgba(30, 64, 175, 0.45);
            }}
            .tts-btn.speaking {{
                background: linear-gradient(135deg, #DC2626 0%, #B91C1C 100%);
                animation: pulse-speaking 1.2s infinite;
            }}
            @keyframes pulse-speaking {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.03); }}
            }}
        </style>
    </head>
    <body>
        <button id="ttsBtn" class="tts-btn" onclick="speakText()">
            <span id="speakerIcon">🔊</span> <span id="btnLabel">{label}</span>
        </button>

        <script>
            let synth = window.speechSynthesis;
            let isSpeaking = false;

            function speakText() {{
                if (!synth) return;
                if (synth.speaking || isSpeaking) {{
                    synth.cancel();
                    stopSpeaking();
                    return;
                }}

                const textToSpeak = '{clean_text}';
                const utterance = new SpeechSynthesisUtterance(textToSpeak);
                utterance.lang = '{locale}';
                utterance.rate = 0.95;

                utterance.onstart = function() {{
                    isSpeaking = true;
                    document.getElementById('ttsBtn').classList.add('speaking');
                    document.getElementById('speakerIcon').innerText = '⏹';
                    document.getElementById('btnLabel').innerText = 'Stop Voice Assist';
                }};

                utterance.onend = function() {{
                    stopSpeaking();
                }};

                utterance.onerror = function() {{
                    stopSpeaking();
                }};

                synth.speak(utterance);
            }}

            function stopSpeaking() {{
                isSpeaking = false;
                document.getElementById('ttsBtn').classList.remove('speaking');
                document.getElementById('speakerIcon').innerText = '🔊';
                document.getElementById('btnLabel').innerText = '{label}';
            }}
        </script>
    </body>
    </html>
    """
    st.components.v1.html(html_code, height=55)
