"""
views/auto_fill.py
==================
Auto-filled scholarship form with AI Suggestions panel — translated via t().
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
import utils.session as session


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=4)

    section_heading(t("autofill_title"), t("autofill_sub"))

    extracted = session.get("extracted_data", {})

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
            session.save_form_data()
            session.navigate("preview")
