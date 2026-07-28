"""
views/help_faq.py
==================
Help & FAQ page for Formitra.
100% Multilingual translation support via t().
Provides step-by-step instructions, voice command guide, scholarship assistance, and Chrome Extension installation details.
Dynamic Light/Dark mode contrast support.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from utils.translations import t
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading(t("faq_page_title"), t("faq_page_sub"))

    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        step_hdr = "#FF7A00"
        step_txt = "#F8FAFC"
    else:
        step_hdr = "#C2410C"
        step_txt = "#1E293B"

    st.markdown(
        f'<div class="card" style="border-left:4px solid #FF7A00;">'
        f'<div style="font-weight:800;font-size:1.05rem;color:{step_hdr};">{t("how_it_works_4steps_title")}</div>'
        f'<div style="margin-top:0.75rem;line-height:1.8;font-size:0.92rem;color:{step_txt};">'
        f'{t("faq_step_1")}<br>'
        f'{t("faq_step_2")}<br>'
        f'{t("faq_step_3")}<br>'
        f'{t("faq_step_4")}'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(f'### {t("faq_sec_hdr")}')

    with st.expander(t("faq_q1_title"), expanded=True):
        st.markdown(t("faq_q1_body"))

    with st.expander(t("faq_q2_title")):
        st.markdown(t("faq_q2_body"))

    with st.expander(t("faq_q3_title")):
        st.markdown(t("faq_q3_body"))

    with st.expander(t("faq_q4_title")):
        st.markdown(t("faq_q4_body"))

    with st.expander(t("faq_q5_title")):
        st.markdown(t("faq_q5_body"))

    spacer()
    info_box(t("faq_helpline_note"))
