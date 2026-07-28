"""
views/ai_processing.py
======================
AI processing page — extracts information from user's audio,
provides Provided vs Required audit, and runs Formitra Eligibility Finder.
100% Multilingual translation support via t().
Dynamic light/dark theme support for ultra-high-contrast rendering.
"""

import time
import streamlit as st

from components.layout          import tricolour_bar, section_heading, spacer
from components.progress        import step_progress_bar
from components.cards           import ai_loader, json_block, field_mapping_row
from utils.constants            import AI_PROCESSING_STEPS
from utils.translations         import t
from utils.gemma_processor      import extract
from utils.voice_assist         import render_voice_assistant_player
from utils.eligibility_engine   import evaluate_eligibility
import utils.session as session

# All fields required for scholarship application
_ALL_REQUIRED_FIELDS = [
    ("Name",        "Full Name"),
    ("City",        "City / District"),
    ("State",       "State"),
    ("Course",      "Course Name"),
    ("Year",        "Current Year"),
    ("Income",      "Annual Family Income"),
    ("DOB",         "Date of Birth"),
    ("Phone",       "Phone Number"),
    ("Email",       "Email Address"),
    ("College",     "College / Institution"),
]


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=2)

    section_heading(t("ai_title"), t("ai_sub"))

    transcript = session.get("transcript", "—")
    language   = session.get("selected_language", "Hindi")

    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        title_color    = "#F8FAFC"
        sub_color      = "#CBD5E1"
        accent_blue    = "#38BDF8"
        banner_bg      = "rgba(5, 150, 105, 0.25)"
        banner_border  = "rgba(5, 150, 105, 0.5)"
        banner_title   = "#34D399"
        banner_text    = "#F8FAFC"
        matched_bg     = "rgba(3, 105, 161, 0.25)"
        matched_border = "rgba(56, 189, 248, 0.5)"
        matched_txt    = "#38BDF8"
        badge_bg_elig  = "rgba(5, 150, 105, 0.3)"
        badge_txt_elig = "#34D399"
        badge_bg_inel  = "rgba(220, 38, 38, 0.3)"
        badge_txt_inel = "#F87171"
        card_bg_prov   = "rgba(5, 150, 105, 0.2)"
        card_txt_prov  = "#34D399"
        card_bg_miss   = "rgba(217, 119, 6, 0.2)"
        card_txt_miss  = "#FBBF24"
    else:
        title_color    = "#0F172A"
        sub_color      = "#475569"
        accent_blue    = "#0284C7"
        banner_bg      = "#ECFDF5"
        banner_border  = "#A7F3D0"
        banner_title   = "#065F46"
        banner_text    = "#047857"
        matched_bg     = "#F0F9FF"
        matched_border = "#BAE6FD"
        matched_txt    = "#0369A1"
        badge_bg_elig  = "#DEF7EC"
        badge_txt_elig = "#03543F"
        badge_bg_inel  = "#FDE8E8"
        badge_txt_inel = "#9B1C1C"
        card_bg_prov   = "#F0FDF4"
        card_txt_prov  = "#065F46"
        card_bg_miss   = "#FFFBEB"
        card_txt_miss  = "#92400E"

    st.markdown(
        f'<div class="card" style="border-left:4px solid #FF7A00;">'
        f'<div style="font-weight:800;font-size:0.85rem;color:#FF7A00;margin-bottom:0.4rem;">'
        f'{t("transcript_used_hdr")}</div>'
        f'<div style="font-size:0.95rem;line-height:1.7;color:{title_color};font-weight:500;">{transcript}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    spacer()

    if not session.get("extraction_done", False):
        _run_simulation(transcript, language)
        st.rerun()
        return

    extracted = session.get("extracted_data", {})

    # Compute Provided vs Missing Required Info
    provided_fields = [label for key, label in _ALL_REQUIRED_FIELDS if key in extracted and extracted[key]]
    missing_fields  = [label for key, label in _ALL_REQUIRED_FIELDS if key not in extracted or not extracted[key]]

    # ── Success & Audit Banner with Voice Assist ───────────────────
    st.markdown(
        f'<div style="background:{banner_bg};border-radius:18px;padding:1.25rem 1.75rem;'
        f'border:1px solid {banner_border};margin-bottom:1.5rem;box-shadow:0 4px 14px rgba(5,150,105,0.1);">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">'
        f'<div style="display:flex;align-items:center;gap:0.75rem;">'
        f'<span style="font-size:1.8rem;">✅</span>'
        f'<div><div style="font-weight:800;font-size:1.1rem;color:{banner_title};">'
        f'{t("voice_proc_success")}</div>'
        f'<div style="font-size:0.9rem;color:{banner_text};margin-top:0.2rem;">'
        f'Extracted <b>{len(provided_fields)} fields</b>. '
        f'<b>{len(missing_fields)} fields</b> require verification.</div>'
        f'</div></div></div></div>',
        unsafe_allow_html=True,
    )

    # ── Formitra Eligibility Finder Card ───────────────────────────
    st.markdown(f'### 🏆 {t("eligibility_finder_title")}')
    eligibility_list = evaluate_eligibility(extracted)
    eligible_count   = sum(1 for e in eligibility_list if e["eligible"])

    st.markdown(
        f'<div style="background:{matched_bg};border:1px solid {matched_border};border-radius:14px;padding:1rem;margin-bottom:1.25rem;">'
        f'<div style="font-weight:800;color:{matched_txt};font-size:0.98rem;">'
        f'🎯 Matched {eligible_count} Govt Scholarship Schemes!</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_e1, col_e2 = st.columns(2)
    for idx, e in enumerate(eligibility_list):
        target_col = col_e1 if idx % 2 == 0 else col_e2
        badge_bg   = badge_bg_elig if e["eligible"] else badge_bg_inel
        badge_txt  = badge_txt_elig if e["eligible"] else badge_txt_inel
        status_tag = t("tag_eligible") if e["eligible"] else t("tag_ineligible")

        with target_col:
            st.markdown(
                f'<div class="card" style="border-top:3px solid {e["badge_color"]};">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="background:{badge_bg};color:{badge_txt};padding:0.25rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:800;">{status_tag}</span>'
                f'<span style="font-size:0.75rem;color:{sub_color};font-weight:600;">{e["badge"]}</span>'
                f'</div>'
                f'<div style="font-weight:800;font-size:1rem;color:{title_color};margin-top:0.5rem;">{e["title"]}</div>'
                f'<div style="font-size:0.85rem;color:{sub_color};margin-top:0.3rem;">{e["desc"]}</div>'
                f'<div style="font-size:0.82rem;color:{accent_blue};margin-top:0.4rem;font-weight:700;">💡 {e["reason"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    spacer()

    # ── Voice Assist Speech Output ────────────────────────────────
    speech_summary_parts = []
    if provided_fields:
        prov_str = ", ".join([f"{k}: {extracted[k]}" for k, _ in _ALL_REQUIRED_FIELDS if k in extracted and extracted[k]])
        speech_summary_parts.append(f"Extracted information: {prov_str}.")
    speech_summary_parts.append(f"You are eligible for {eligible_count} government scholarship schemes.")
    if missing_fields:
        miss_str = ", ".join(missing_fields)
        speech_summary_parts.append(f"Please provide missing fields: {miss_str}.")

    tts_script = " ".join(speech_summary_parts)

    st.markdown(f'### {t("voice_assist_title")}')
    render_voice_assistant_player(text=tts_script, language=language, label=f"🔊 {t('voice_assist_title')} ({language})")

    spacer()

    # ── Information Breakdown Cards ────────────────────────────────
    c_prov, c_miss = st.columns(2)

    with c_prov:
        prov_list = "".join(f'<li style="margin-bottom:0.3rem;"><b>{f}</b>: {extracted.get(k, "")}</li>' for k, f in _ALL_REQUIRED_FIELDS if k in extracted and extracted[k])
        if not prov_list:
            prov_list = '<li>No fields identified directly. Please check transcript.</li>'
        st.markdown(
            f'<div class="card" style="border-left:4px solid #10B981;background:{card_bg_prov};">'
            f'<div style="font-weight:800;font-size:0.95rem;color:{card_txt_prov};margin-bottom:0.5rem;">'
            f'{t("provided_audio_title")} ({len(provided_fields)})</div>'
            f'<ul style="font-size:0.88rem;color:{title_color};padding-left:1.2rem;margin:0;">{prov_list}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with c_miss:
        miss_list = "".join(f'<li style="margin-bottom:0.3rem;"><b>{f}</b> (Required)</li>' for f in missing_fields)
        if not miss_list:
            miss_list = '<li>All required information was provided in your voice! 🎉</li>'
        st.markdown(
            f'<div class="card" style="border-left:4px solid #F59E0B;background:{card_bg_miss};">'
            f'<div style="font-weight:800;font-size:0.95rem;color:{card_txt_miss};margin-bottom:0.5rem;">'
            f'{t("missing_info_title")} ({len(missing_fields)})</div>'
            f'<ul style="font-size:0.88rem;color:{title_color};padding-left:1.2rem;margin:0;">{miss_list}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )

    spacer()

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        section_heading(t("extracted_json_title"), t("extracted_json_sub"))
        json_block(extracted)

    with right_col:
        section_heading(t("field_mapping_title"), t("field_mapping_sub"))
        for key, label in _ALL_REQUIRED_FIELDS:
            val   = extracted.get(key, "—")
            found = key in extracted and bool(extracted[key])
            field_mapping_row(label=label, value=val, found=found)

    spacer()
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.button(t("extract_info_btn"), use_container_width=True, type="primary"):
            session.navigate("auto_fill")


# ─── Private helpers ───────────────────────────────────────────────

def _run_simulation(transcript: str, language: str) -> None:
    placeholder = st.empty()
    for icon, msg, duration in AI_PROCESSING_STEPS:
        placeholder.markdown(
            ai_loader(step_icon=icon, step_message=msg),
            unsafe_allow_html=True,
        )
        time.sleep(duration)
    placeholder.empty()

    result = extract(transcript=transcript, language=language)
    session.set("extracted_data",  result.data)
    session.set("extraction_done", True)
