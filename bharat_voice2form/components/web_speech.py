"""
components/web_speech.py
========================
Live streaming speech dictation component.
Performs real-time HTML5 browser speech-to-text in 8 Indian languages.
Renders inline HTML to prevent path resolution issues when directory paths contain spaces.
"""

from __future__ import annotations

import os
import streamlit as st
import streamlit.components.v1 as components

_LOCALE_MAP: dict[str, str] = {
    "Hindi":     "hi-IN",
    "Tamil":     "ta-IN",
    "Telugu":    "te-IN",
    "Bengali":   "bn-IN",
    "Marathi":   "mr-IN",
    "Kannada":   "kn-IN",
    "Malayalam": "ml-IN",
    "English":   "en-IN",
}

# Path to index.html
_PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
_INDEX_HTML_PATH = os.path.join(_PARENT_DIR, "web_speech_comp", "index.html")


def render_live_speech_dictation(language: str = "Hindi", is_dark: bool = True) -> str | None:
    """
    Render HTML5 live speech transcription component reliably without static server path bugs.
    """
    locale = _LOCALE_MAP.get(language, "hi-IN")
    theme_class = "dark-theme" if is_dark else "light-theme"

    try:
        with open(_INDEX_HTML_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Inject dynamic locale, language name, and theme class into HTML template
        html_content = html_content.replace('targetLocale = "hi-IN";', f'targetLocale = "{locale}";')
        html_content = html_content.replace('languageName = "Hindi";', f'languageName = "{language}";')
        html_content = html_content.replace('<body class="dark-theme">', f'<body class="{theme_class}">')

        # Render inline HTML safely
        components.html(html_content, height=210, scrolling=False)
    except Exception as exc:
        st.warning(f"⚠️ Live dictation widget initialization note: {exc}")

    return None
