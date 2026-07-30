"""
views/voice_input.py
====================
Voice input page — live streaming dictation & audio recording with Language Auto-Detector.
100% Multilingual translation support via t().
Dynamic Light/Dark mode contrast support.
"""

import hashlib
import streamlit as st

from components.layout     import tricolour_bar, section_heading, info_box, spacer
from components.progress   import step_progress_bar
from components.waveform   import speech_tips_card
from components.web_speech import render_live_speech_dictation
from utils.translations    import t, get_available_languages
from utils.speech_to_text  import transcribe, ENGINE
from utils.lang_detector   import detect_language
from utils.voice_assist    import render_voice_assistant_player
import utils.session as session


def _update_transcript(text: str) -> None:
    """Synchronise transcript state across session and text-area widget key."""
    clean_text = text.strip()
    session.set("transcript", clean_text)
    st.session_state["transcript"] = clean_text
    st.session_state["transcript_editor"] = clean_text

    # Auto-detect language if script indicates non-English/Devanagari
    detected = detect_language(clean_text)
    session.set("detected_language", detected)


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=1)

    form_name = session.get("selected_form") or "Post-Matric Scholarship Scheme"
    is_dark   = st.session_state.get("dark_mode", False)

    badge_bg     = "rgba(255, 122, 0, 0.2)" if is_dark else "#FFF7ED"
    badge_txt    = "#FF7A00" if is_dark else "#C2410C"
    badge_border = "rgba(255, 122, 0, 0.5)" if is_dark else "#FFEDD5"
    sub_color    = "#CBD5E1" if is_dark else "#475569"

    st.markdown(
        f'<div style="margin-bottom:1.25rem;">'
        f'<span style="background:{badge_bg};color:{badge_txt} !important;'
        f'border-radius:10px;padding:0.45rem 1rem;font-size:0.88rem;font-weight:800;'
        f'border:1px solid {badge_border};display:inline-block;">'
        f'📋 {t("selected_scheme_badge")}: {form_name}</span></div>',
        unsafe_allow_html=True,
    )

    section_heading(t("voice_title"), t("voice_sub"))

    left_col, right_col = st.columns([1, 1], gap="large")

    # ── Left Column: Live Speech Dictation & Audio File Recorder ───
    with left_col:
        langs        = get_available_languages()
        current_lang = session.get("selected_language", "Hindi")
        try:
            lang_idx = langs.index(current_lang)
        except ValueError:
            lang_idx = 0

        lang = st.selectbox(
            t("select_language"),
            langs,
            index=lang_idx,
            key="lang_select",
        )
        if lang != current_lang:
            session.set("selected_language", lang)
            st.rerun()

        # Language Auto-Detector Badge
        if det_lang := session.get("detected_language"):
            st.markdown(
                f'<div style="background:#ECFDF5;border:1px solid #6EE7B7;border-radius:8px;'
                f'padding:0.4rem 0.8rem;font-size:0.82rem;color:#065F46;font-weight:700;'
                f'margin-bottom:0.75rem;">'
                f'🌐 Auto-Detected Speech Language: <u>{det_lang}</u></div>',
                unsafe_allow_html=True,
            )

        # ── 1. Live Streaming Dictation Component ───────────────────
        st.markdown(
            f'<div style="font-weight:800;font-size:1rem;color:#FF7A00;margin:0.5rem 0 0.4rem;">'
            f'{t("live_dictation_title")}</div>'
            f'<div style="display:inline-flex;align-items:center;gap:0.4rem;background:rgba(249,115,22,0.1);'
            f'border:1px solid rgba(249,115,22,0.3);border-radius:20px;padding:0.2rem 0.7rem;'
            f'font-size:0.75rem;font-weight:700;color:#F97316;margin-bottom:0.5rem;">'
            f'⚡ Powered by Groq Whisper Large V3 Turbo</div>',
            unsafe_allow_html=True,
        )
        live_text = render_live_speech_dictation(language=lang, is_dark=is_dark)

        if live_text and isinstance(live_text, str) and live_text.strip():
            _update_transcript(live_text)

        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,122,0,0.2);margin:1.25rem 0;'>", unsafe_allow_html=True)

        # ── 2. Microphone Audio File Clip Recorder ─────────────────
        st.markdown(
            f'<div style="font-weight:800;font-size:1rem;color:#FF7A00;margin-bottom:0.4rem;">'
            f'{t("audio_recorder_title")}</div>',
            unsafe_allow_html=True,
        )
        audio_value = st.audio_input(
            t("audio_record_prompt"),
            key="audio_clip_recorder",
        )

        if audio_value is not None:
            audio_bytes = audio_value.read()
            audio_hash  = hashlib.md5(audio_bytes).hexdigest()

            if session.get("last_audio_hash") != audio_hash:
                session.set("last_audio_hash", audio_hash)
                with st.spinner(f"🎙️ Transcribing audio clip in {lang}…"):
                    result = transcribe(audio_bytes=audio_bytes, language=lang)

                if result and result.text:
                    _update_transcript(result.text)
                    st.toast(f"✅ Audio transcribed ({result.engine})")
                    st.rerun()
                else:
                    err = result.error or "Could not transcribe audio"
                    st.error(f"⚠️ {err}")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button(
            t("load_sample_btn"),
            use_container_width=True,
            type="primary",
            help="Load a sample transcript for demonstration",
        ):
            result = transcribe(audio_bytes=None, language=lang)
            _update_transcript(result.text)
            st.rerun()

        info_box(t("demo_note"))

    # ── Right Column: Active Transcribed Speech Display ────────────
    with right_col:
        section_heading(t("active_speech_title"), t("active_speech_sub"))

        if "transcript_editor" not in st.session_state:
            st.session_state["transcript_editor"] = session.get("transcript", "")

        transcript = st.text_area(
            "Transcribed Speech (editable)",
            height=280,
            placeholder=t("dictation_placeholder"),
            key="transcript_editor",
        )
        session.set("transcript", transcript)

        if transcript.strip():
            render_voice_assistant_player(
                text=transcript,
                language=lang,
                label=f"🔊 Listen to Transcript in {lang}",
            )

        st.markdown(
            f'<div style="font-size:0.8rem;color:{sub_color};margin-bottom:0.75rem;margin-top:0.5rem;">'
            f'🔧 Active STT Engine: <code style="background:rgba(255,122,0,0.1);padding:0.2rem 0.5rem;border-radius:4px;">'
            f'{ENGINE} / Live WebSpeech</code></div>',
            unsafe_allow_html=True,
        )

        speech_tips_card()

    # ── Extract Button & Navigation ────────────────────────────────
    spacer()
    _, center, _ = st.columns([1, 2, 1])
    with center:
        active_transcript = session.get("transcript", "").strip()
        has_transcript    = bool(active_transcript)

        if st.button(
            t("extract_info_btn"),
            use_container_width=True,
            type="primary",
            disabled=not has_transcript,
        ):
            session.reset_extraction()
            session.navigate("ai_processing")

    if not has_transcript:
        st.markdown(
            f'<div style="text-align:center;font-size:0.85rem;color:{sub_color};margin-top:0.4rem;font-weight:500;">'
            f'{t("no_transcript")}'
            f'</div>',
            unsafe_allow_html=True,
        )
