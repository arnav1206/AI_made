"""
components/waveform.py
======================
Audio waveform animation and microphone-widget components
used on the Voice Input page.
"""

from __future__ import annotations

import streamlit as st


def waveform(visible: bool = True) -> None:
    """
    Render the animated waveform bars.

    Parameters
    ----------
    visible : bool
        If False the waveform is hidden (call when not recording).
    """
    if not visible:
        return

    bars = "".join(
        f'<div class="waveform-bar"></div>' for _ in range(10)
    )
    st.markdown(
        f'<div class="waveform">{bars}</div>',
        unsafe_allow_html=True,
    )


def mic_widget(is_recording: bool, language: str) -> None:
    """
    Render the microphone status card.

    Parameters
    ----------
    is_recording : bool
        When True the widget shows a red "Recording…" state.
        When False it shows the idle blue "Tap to Record" state.
    language : str
        Current selected language — shown in the sub-label.
    """
    mic_color = "#EF4444" if is_recording else "#FF7A00"
    mic_bg    = "linear-gradient(135deg,rgba(239,68,68,0.2),rgba(239,68,68,0.1))" if is_recording \
                else "linear-gradient(135deg,rgba(255,122,0,0.2),rgba(255,122,0,0.1))"
    mic_icon  = "⏹️" if is_recording else "🎙️"
    mic_label = "Recording…" if is_recording else "Tap to Record"
    sub_label = (
        f"Recording in {language}…" if is_recording
        else "Click the button below to start"
    )

    st.markdown(
        f'<div class="mic-container" style="background:{mic_bg};border:1px solid rgba(255,122,0,0.4);border-radius:14px;padding:1rem;text-align:center;">'
        f'<div class="mic-icon" style="font-size:2rem;margin-bottom:0.4rem;">{mic_icon}</div>'
        f'<div style="font-weight:800;font-size:1.05rem;color:{mic_color};">{mic_label}</div>'
        f'<div style="font-size:0.83rem;color:#F8FAFC;opacity:0.85;margin-top:0.25rem;">{sub_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Show animated waveform only while recording
    waveform(visible=is_recording)


def speech_tips_card() -> None:
    """Render the 'Speech Tips' guidance card shown on the voice input page."""
    st.markdown(
        '<div class="card" style="margin-top:0.5rem;">'
        '<div style="font-weight:800;font-size:0.95rem;color:#FF7A00;margin-bottom:0.5rem;">💬 Speech Tips & Recommendations</div>'
        '<ul style="margin:0;padding-left:1.2rem;font-size:0.85rem;color:#F8FAFC;line-height:1.8;">'
        '<li>Speak your full name clearly</li>'
        '<li>Mention your city / district</li>'
        '<li>State your course and year of study</li>'
        '<li>Say your family income in words</li>'
        '<li>Include phone / email if available</li>'
        '</ul></div>',
        unsafe_allow_html=True,
    )
