"""
components/waveform.py
======================
Audio waveform animation and microphone-widget components
used on the Voice Input page with dynamic light/dark theme support.
100% Multilingual translation support via t().
"""

from __future__ import annotations

import streamlit as st
from utils.translations import t
import utils.session as session


def waveform(visible: bool = True) -> None:
    """Render the animated waveform bars."""
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
    """Render the microphone status card."""
    is_dark   = st.session_state.get("dark_mode", True)
    mic_color = "#EF4444" if is_recording else "#FF7A00"
    sub_color = "#F8FAFC" if is_dark else "#475569"
    mic_bg    = "linear-gradient(135deg,rgba(239,68,68,0.2),rgba(239,68,68,0.1))" if is_recording \
                else "linear-gradient(135deg,rgba(255,122,0,0.15),rgba(255,122,0,0.05))"
    mic_icon  = "⏹️" if is_recording else "🎙️"
    mic_label = t("recording_active") if is_recording else t("tap_to_record")
    sub_label = (
        f"{t('recording_in')} {language}…" if is_recording
        else t("click_to_start")
    )

    st.markdown(
        f'<div class="mic-container" style="background:{mic_bg};border:1px solid rgba(255,122,0,0.4);border-radius:14px;padding:1rem;text-align:center;">'
        f'<div class="mic-icon" style="font-size:2rem;margin-bottom:0.4rem;">{mic_icon}</div>'
        f'<div style="font-weight:800;font-size:1.05rem;color:{mic_color};">{mic_label}</div>'
        f'<div style="font-size:0.83rem;color:{sub_color};margin-top:0.25rem;">{sub_label}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # Show animated waveform only while recording
    waveform(visible=is_recording)


def speech_tips_card() -> None:
    """Render the 'Required Form Fields' guidance card on the voice input page."""
    is_dark    = st.session_state.get("dark_mode", True)
    text_col   = "#F8FAFC" if is_dark else "#475569"
    card_bg    = "#151C2C" if is_dark else "#FFFFFF"
    border_c   = "rgba(255, 122, 0, 0.4)" if is_dark else "#FED7AA"
    dynamic_qs = session.get("dynamic_form_questions")
    extracted  = session.get("extracted_data", {})
    is_g_form  = bool(dynamic_qs) or session.get("is_google_form_imported") or ("Google Form" in str(session.get("selected_form")))

    std_keys    = {"Name", "DOB", "Gender", "Category", "Address", "City", "State", "PIN Code", "College", "Course", "Year", "Income", "Phone", "Email", "Percentage", "Full Name", "Date of Birth", "Annual Family Income"}
    custom_keys = [k for k in extracted.keys() if k and k not in std_keys]

    if dynamic_qs:
        badge_html = (
            f'<div style="background:rgba(5, 150, 105, 0.15);border:1px solid rgba(5, 150, 105, 0.4);'
            f'color:#10B981;border-radius:6px;padding:0.3rem 0.65rem;font-size:0.78rem;font-weight:800;'
            f'margin-bottom:0.6rem;display:inline-block;">'
            f'✨ {len(dynamic_qs)} Google Form Questions Extracted & Ready for Voice</div>'
        )
        q_items = []
        for q in dynamic_qs:
            req_tag = ' <span style="color:#EF4444;">*</span>' if q.get("required") else ""
            q_items.append(f'<li>📋 <strong>{q["title"]}</strong>{req_tag}</li>')
        list_html = "".join(q_items)
        title_text = f"📋 Imported Google Form Questions ({len(dynamic_qs)} Fields)"
    elif custom_keys or is_g_form:
        keys_to_show = custom_keys if custom_keys else list(extracted.keys())
        badge_html = (
            f'<div style="background:rgba(5, 150, 105, 0.15);border:1px solid rgba(5, 150, 105, 0.4);'
            f'color:#10B981;border-radius:6px;padding:0.3rem 0.65rem;font-size:0.78rem;font-weight:800;'
            f'margin-bottom:0.6rem;display:inline-block;">'
            f'✨ {len(keys_to_show)} Imported Form Questions Ready for Voice</div>'
        )
        list_html = "".join([f'<li>📋 <strong>{k}</strong></li>' for k in keys_to_show])
        title_text = f"📋 Imported Form Questions ({len(keys_to_show)} Fields)"
    else:
        title_text = "📋 Required Form Fields to Dictate"
        badge_html = ""
        list_html = (
            f'<li>👤 <strong>Full Name & Date of Birth</strong></li>'
            f'<li>🏷️ <strong>Gender & Category (SC/ST/OBC/General)</strong></li>'
            f'<li>📍 <strong>Full Residential Address & State</strong></li>'
            f'<li>🎓 <strong>College Name & Course Name</strong></li>'
            f'<li>📅 <strong>Current Academic Year & Marks (Percentage/CGPA)</strong></li>'
            f'<li>💼 <strong>Annual Family Income (in INR)</strong></li>'
            f'<li>📞 <strong>Mobile Phone Number</strong></li>'
        )

    st.markdown(
        f'<div class="card" style="background:{card_bg};border:1px solid {border_c};border-radius:14px;padding:1.1rem;">'
        f'{badge_html}'
        f'<div style="font-weight:800;font-size:0.96rem;color:#FF7A00;margin-bottom:0.4rem;">{title_text}</div>'
        f'<div style="font-size:0.8rem;color:{text_col};opacity:0.85;margin-bottom:0.75rem;">'
        f'Speak into the mic to provide answers for these form questions:</div>'
        f'<ul style="font-size:0.84rem;color:{text_col};line-height:1.9;padding-left:1.2rem;margin:0;">'
        f'{list_html}'
        f'</ul>'
        f'</div>',
        unsafe_allow_html=True,
    )
