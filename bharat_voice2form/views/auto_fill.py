"""
views/auto_fill.py
==================
Auto-filled scholarship form with AI Suggestions panel & Missing Fields Voice Prompter.
100% Multilingual translation support via t().
"""

import streamlit as st

from components.layout      import (
    tricolour_bar, section_heading, form_card_open, form_card_close, spacer
)
from components.progress    import step_progress_bar
from components.form_fields import (
    personal_info_fields, address_fields,
    academic_fields, financial_contact_fields,
)
from components.suggestions import render_panel as render_suggestions
from utils.translations     import t
from utils.voice_assist     import render_voice_assistant_player
import utils.session as session


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=4)

    section_heading(t("autofill_title"), t("autofill_sub"))

    extracted = session.get("extracted_data", {})
    language  = session.get("selected_language", "Hindi")

    # ── Missing Required Fields Detector & AI Voice Assistant ──────
    required_map = [
        ("field_name", "Full Name", t("reg_name", "Full Name")),
        ("field_dob", "Date of Birth", t("lbl_dob", "Date of Birth")),
        ("field_income", "Annual Family Income", t("lbl_income", "Annual Family Income")),
        ("field_state", "State", t("reg_state", "State")),
        ("field_college", "Institute Name", t("lbl_college", "Institute Name")),
    ]

    missing_keys = []
    missing_labels_en = []
    missing_labels_hi = []

    for f_key, lbl_en, lbl_hi in required_map:
        val = session.get(f_key, "").strip()
        if not val:
            missing_keys.append(f_key)
            missing_labels_en.append(lbl_en)
            missing_labels_hi.append(lbl_hi)

    if missing_keys:
        if language == "Hindi":
            missing_str = ", ".join(missing_labels_hi)
            tts_prompt  = f"ध्यान दें! आपके फॉर्म में {len(missing_keys)} आवश्यक जानकारी अधूरी है: {missing_str}। कृपया माइक बटन दबाकर इन बची हुई जानकारियों को बोलें।"
        else:
            missing_str = ", ".join(missing_labels_en)
            tts_prompt  = f"Attention! {len(missing_keys)} required fields are missing in your form: {missing_str}. Please click the microphone button to dictate these remaining details."

        is_dark = st.session_state.get("dark_mode", False)
        card_bg = "rgba(217, 119, 6, 0.18)" if is_dark else "#FFFBEB"
        card_border = "rgba(245, 158, 11, 0.6)" if is_dark else "#FDE68A"
        txt_col = "#FBBF24" if is_dark else "#92400E"

        st.markdown(
            f'<div class="card" style="background:{card_bg};border:1px solid {card_border};margin-bottom:1.5rem;">'
            f'<div style="font-weight:800;font-size:1.05rem;color:{txt_col};margin-bottom:0.4rem;">'
            f'🤖 Formitra AI Assistant: {len(missing_keys)} Required Fields Missing</div>'
            f'<div style="font-size:0.88rem;color:{txt_col};line-height:1.6;margin-bottom:0.75rem;">'
            f'{tts_prompt}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        c_prompt1, c_prompt2 = st.columns([2, 1])
        with c_prompt1:
            render_voice_assistant_player(text=tts_prompt, language=language, label=f"🔊 {t('listen_missing_req')} ({language})")
        with c_prompt2:
            if st.button(t("dictate_missing_btn"), use_container_width=True, type="primary"):
                session.navigate("voice_input")

        spacer(0.5)

    form_col, tip_col = st.columns([3, 2], gap="large")

    # ── Left: Form sections ────────────────────────────────────────
    with form_col:
        form_card_open("👤", t("section_personal").replace("👤 ", ""))
        personal_info_fields(extracted)
        form_card_close()

        form_card_open("📍", t("section_address").replace("📍 ", ""))
        address_fields(extracted)
        form_card_close()

        form_card_open("🎓", t("section_academic").replace("🎓 ", ""))
        academic_fields(extracted)
        form_card_close()

        form_card_open("💰", t("section_financial").replace("💰 ", ""))
        financial_contact_fields(extracted)
        form_card_close()

    # ── Right: AI Suggestions ──────────────────────────────────────
    with tip_col:
        render_suggestions(extracted=extracted, total_fields=15)

    # ── Action buttons ─────────────────────────────────────────────
    spacer()
    _, b1, b2, b3, _ = st.columns([1, 1.5, 1.5, 1.5, 1])

    with b1:
        if st.button(t("btn_re_record"), use_container_width=True):
            session.reset_extraction()
            session.reset_recording()
            session.navigate("voice_input")

    with b2:
        if st.button(t("btn_clear"), use_container_width=True):
            session.reset_form_fields()
            st.rerun()

    with b3:
        if st.button(t("btn_preview"), use_container_width=True, type="primary"):
            gender   = st.session_state.get("field_gender", "— Select —")
            category = st.session_state.get("field_category", "— Select —")
            state    = st.session_state.get("field_state", "— Select —")
            year     = st.session_state.get("field_year", "— Select —")
            name     = st.session_state.get("field_name", "").strip()

            unselected = []
            if not name:
                unselected.append("Full Name")
            if gender == "— Select —":
                unselected.append("Gender")
            if category == "— Select —":
                unselected.append("Category")
            if state in ("— Select —", "— Select State —"):
                unselected.append("State of Domicile")
            if year == "— Select —":
                unselected.append("Current Academic Year")

            if unselected:
                st.warning(f"⚠️ Pre-Submission Alert: Please select/provide valid options for: **{', '.join(unselected)}** before proceeding.")
            else:
                session.save_form_data()
                session.navigate("preview")
