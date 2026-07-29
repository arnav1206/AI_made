"""
components/web_speech.py
========================
Live streaming speech dictation component.
Performs real-time HTML5 browser speech-to-text in 8 Indian languages.
Uses Streamlit Custom bidirectional components to return values back to Python.
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

# Get current path to components folder
parent_dir = os.path.dirname(os.path.abspath(__file__))
comp_dir = os.path.join(parent_dir, "web_speech_comp")

# Declare custom bidirectional WebSpeech component
_web_speech_component = components.declare_component("web_speech_component", path=comp_dir)


def render_live_speech_dictation(language: str = "Hindi", is_dark: bool = True) -> str | None:
    """
    Render HTML5 live speech transcription component.

    Parameters
    ----------
    language : str
        Target language name (e.g. "Hindi", "Tamil", "English").
    is_dark : bool
        Whether Dark mode is currently active.

    Returns
    -------
    str | None
        Live transcribed speech text.
    """
    locale = _LOCALE_MAP.get(language, "hi-IN")
    
    # Return the real-time values from the bidirectional component
    return _web_speech_component(
        language=language,
        locale=locale,
        is_dark=is_dark,
        key="web_speech_dictation_comp"
    )
