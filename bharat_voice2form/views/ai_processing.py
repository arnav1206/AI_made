"""
views/ai_processing.py
======================
AI processing page — extracts information from user's audio,
provides Provided vs Required audit, and runs Formitra Eligibility Finder.
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
    step_progress_bar(current_step=3)

    section_heading(t("ai_title"), t("ai_sub"))

    transcript = session.get("transcript", "—")
    language   = session.get("selected_language", "Hindi")

    st.markdown(
        f'<div class="card" style="border-left:4px solid #FF7A00;">'
        f'<div style="font-weight:800;font-size:0.85rem;color:#FF7A00;margin-bottom:0.4rem;">'
        f'🎙️ YOUR SPEECH TRANSCRIPT USED</div>'
        f'<div style="font-size:0.95rem;line-height:1.7;color:#F8FAFC;font-weight:500;">{transcript}</div>'
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
        f'<div style="background:rgba(5, 150, 105, 0.25);'
        f'border-radius:18px;padding:1.25rem 1.75rem;border:1px solid rgba(5, 150, 105, 0.5);'
        f'margin-bottom:1.5rem;box-shadow:0 4px 14px rgba(5,150,105,0.1);">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:1rem;">'
        f'<div style="display:flex;align-items:center;gap:0.75rem;">'
        f'<span style="font-size:1.8rem;">✅</span>'
        f'<div><div style="font-weight:800;font-size:1.1rem;color:#34D399;">'
        f'Voice Information Processed Successfully!</div>'
        f'<div style="font-size:0.9rem;color:#F8FAFC;margin-top:0.2rem;">'
        f'Extracted <b>{len(provided_fields)} fields</b> from your speech audio. '
        f'<b>{len(missing_fields)} fields</b> require manual verification.</div>'
        f'</div></div></div></div>',
        unsafe_allow_html=True,
    )

    # ── Formitra Eligibility Finder Card ───────────────────────────
    st.markdown("### 🏆 Formitra Scholarship Eligibility Finder")
    eligibility_list = evaluate_eligibility(extracted)
    eligible_count   = sum(1 for e in eligibility_list if e["eligible"])

    st.markdown(
        f'<div style="background:rgba(3, 105, 161, 0.25);border:1px solid rgba(56, 189, 248, 0.5);border-radius:14px;padding:1rem;margin-bottom:1.25rem;">'
        f'<div style="font-weight:800;color:#38BDF8;font-size:0.98rem;">'
        f'🎯 Matched {eligible_count} Govt Scholarship Schemes for your profile!</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    col_e1, col_e2 = st.columns(2)
    for idx, e in enumerate(eligibility_list):
        target_col = col_e1 if idx % 2 == 0 else col_e2
        badge_bg   = "rgba(5, 150, 105, 0.3)" if e["eligible"] else "rgba(220, 38, 38, 0.3)"
        badge_txt  = "#34D399" if e["eligible"] else "#F87171"
        status_tag = "ELIGIBLE ✅" if e["eligible"] else "INELIGIBLE ❌"

        with target_col:
            st.markdown(
                f'<div class="card" style="border-top:3px solid {e["badge_color"]};">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="background:{badge_bg};color:{badge_txt};padding:0.25rem 0.6rem;border-radius:20px;font-size:0.75rem;font-weight:800;">{status_tag}</span>'
                f'<span style="font-size:0.75rem;color:#CBD5E1;font-weight:600;">{e["badge"]}</span>'
                f'</div>'
                f'<div style="font-weight:800;font-size:1rem;color:#F8FAFC;margin-top:0.5rem;">{e["title"]}</div>'
                f'<div style="font-size:0.85rem;color:#CBD5E1;margin-top:0.3rem;">{e["desc"]}</div>'
                f'<div style="font-size:0.82rem;color:#38BDF8;margin-top:0.4rem;font-weight:700;">💡 {e["reason"]}</div>'
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

    st.markdown("### 🔊 Voice Assist Audit Summary")
    render_voice_assistant_player(text=tts_script, language=language, label=f"🔊 Listen to Voice Assist ({language})")

    spacer()

    # ── Information Breakdown Cards ────────────────────────────────
    c_prov, c_miss = st.columns(2)

    with c_prov:
        prov_list = "".join(f'<li style="margin-bottom:0.3rem;"><b>{f}</b>: {extracted.get(k, "")}</li>' for k, f in _ALL_REQUIRED_FIELDS if k in extracted and extracted[k])
        if not prov_list:
            prov_list = '<li>No fields identified directly. Please check transcript.</li>'
        st.markdown(
            f'<div class="card" style="border-left:4px solid #10B981;background:rgba(5, 150, 105, 0.2);">'
            f'<div style="font-weight:800;font-size:0.95rem;color:#34D399;margin-bottom:0.5rem;">'
            f'✅ Provided from Audio ({len(provided_fields)})</div>'
            f'<ul style="font-size:0.88rem;color:#F8FAFC;padding-left:1.2rem;margin:0;">{prov_list}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with c_miss:
        miss_list = "".join(f'<li style="margin-bottom:0.3rem;"><b>{f}</b> (Required)</li>' for f in missing_fields)
        if not miss_list:
            miss_list = '<li>All required information was provided in your voice! 🎉</li>'
        st.markdown(
            f'<div class="card" style="border-left:4px solid #F59E0B;background:rgba(217, 119, 6, 0.2);">'
            f'<div style="font-weight:800;font-size:0.95rem;color:#FBBF24;margin-bottom:0.5rem;">'
            f'⚠️ Missing Information Needed ({len(missing_fields)})</div>'
            f'<ul style="font-size:0.88rem;color:#F8FAFC;padding-left:1.2rem;margin:0;">{miss_list}</ul>'
            f'</div>',
            unsafe_allow_html=True,
        )

    spacer()

    left_col, right_col = st.columns([1, 1], gap="large")

    with left_col:
        section_heading("📦 Extracted JSON", "Structured data generated from speech")
        json_block(extracted)

    with right_col:
        section_heading(t("field_mapping"), t("field_mapping_sub"))
        for key, label in _ALL_REQUIRED_FIELDS:
            val   = extracted.get(key, "—")
            found = key in extracted and bool(extracted[key])
            field_mapping_row(label=label, value=val, found=found)

    spacer()
    _, center, _ = st.columns([1, 2, 1])
    with center:
        if st.button("📝 Auto-Fill Form & Complete Missing Info →", use_container_width=True, type="primary"):
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
