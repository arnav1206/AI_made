"""
views/home.py
=============
Home page for Formitra — AI Voice-Powered Scholarship Portal.
Features dynamic Light/Dark mode hero banner, ultra-high-contrast typography,
and dynamic Multilingual Speech Orbit image assets for Light and Dark themes.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from components.cards  import step_card, feature_badge
from utils.constants   import SCHOLARSHIP_FORMS
from utils.translations import t
import utils.session as session


def render() -> None:
    tricolour_bar()

    is_dark = st.session_state.get("dark_mode", False)
    if is_dark:
        hero_bg     = "linear-gradient(135deg, #1E1B4B 0%, #312E81 50%, #4F46E5 100%)"
        hero_border = "1px solid rgba(129, 140, 248, 0.4)"
        hero_shadow = "0 20px 40px rgba(79, 70, 229, 0.35)"
        img_path    = "bharat_voice2form/assets/images/multilingual_dark.jpg"
    else:
        hero_bg     = "linear-gradient(135deg, #0F172A 0%, #003B95 50%, #FF7A00 100%)"
        hero_border = "1px solid rgba(255, 255, 255, 0.2)"
        hero_shadow = "0 20px 40px rgba(0, 40, 104, 0.25)"
        img_path    = "bharat_voice2form/assets/images/multilingual_light.jpg"

    # ── Hero Section with Multilingual Orbit Diagram ───────────────
    h_col1, h_col2 = st.columns([1.3, 1], gap="large")

    with h_col1:
        st.markdown(
            f'<div class="hero-banner" style="background:{hero_bg};'
            f'border-radius:24px;padding:2.5rem 2rem;color:#FFFFFF !important;'
            f'box-shadow:{hero_shadow};border:{hero_border};margin-bottom:1rem;">'
            f'<div style="font-size:2.8rem;margin-bottom:0.4rem;">🎙️</div>'
            f'<h1 style="font-size:2.2rem;font-weight:900;margin:0;letter-spacing:-0.5px;color:#FFFFFF !important;text-shadow:0 2px 12px rgba(0,0,0,0.5);">'
            f'{t("hero_title")}</h1>'
            f'<p style="font-size:1.05rem;color:#F8FAFC !important;opacity:0.95;margin-top:0.85rem;line-height:1.6;">'
            f'{t("hero_sub")}</p>'
            f'<div style="margin-top:1.5rem;display:flex;gap:0.75rem;flex-wrap:wrap;">'
            f'<span style="background:rgba(255,255,255,0.18);backdrop-filter:blur(8px);color:#FFFFFF !important;'
            f'padding:0.45rem 1rem;border-radius:50px;font-weight:800;font-size:0.85rem;border:1px solid rgba(255,255,255,0.3);">'
            f'🇮🇳 9 Official Indian Languages</span>'
            f'<span style="background:rgba(255,255,255,0.18);backdrop-filter:blur(8px);color:#FFFFFF !important;'
            f'padding:0.45rem 1rem;border-radius:50px;font-weight:800;font-size:0.85rem;border:1px solid rgba(255,255,255,0.3);">'
            f'🤖 Gemma AI Multilingual Engine</span>'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with h_col2:
        st.image(
            img_path,
            use_container_width=True,
            caption="🌐 Formitra Multilingual Voice Orbit Architecture",
        )

    # ── Action Buttons ─────────────────────────────────────────────
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("🚀 Start Voice Application →", use_container_width=True, type="primary"):
            session.navigate("form_selection")

        if st.button("🔍 Track Existing Application / Login", use_container_width=True):
            session.navigate("track_status")

    spacer()

    # ── 4-Step Process ──────────────────────────────────────────────
    section_heading("⚡ How Formitra Works", "4 easy steps to complete your government application")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        step_card(1, "📋 Select Scheme", "Pick your scholarship application scheme", "🎓")
    with col2:
        step_card(2, "🎙️ Voice Dictation", "Speak your details in your mother tongue", "🗣️")
    with col3:
        step_card(3, "🤖 AI Auto-Fill", "Gemma AI maps your speech to form fields", "✨")
    with col4:
        step_card(4, "🎉 Track Reference", "Submit & track application status anytime", "📄")

    spacer()

    # ── Popular Scholarship Schemes ───────────────────────────────
    section_heading("🏛️ Government Scholarship Schemes Available", "Voice-supported official scholarship applications")

    sc_cols = st.columns(2)
    for idx, sf in enumerate(SCHOLARSHIP_FORMS):
        target_col = sc_cols[idx % 2]
        with target_col:
            st.markdown(
                f'<div class="card" style="border-left:4px solid {sf["tag_color"]};">'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<span style="font-size:1.8rem;">{sf["icon"]}</span>'
                f'<span style="background:{sf["tag_color"]}15;color:{sf["tag_color"]};padding:0.25rem 0.65rem;border-radius:20px;font-size:0.75rem;font-weight:800;">{sf["tag"]}</span>'
                f'</div>'
                f'<div style="font-size:1.1rem;font-weight:800;margin-top:0.75rem;">{sf["title"]}</div>'
                f'<div style="font-size:0.88rem;opacity:0.8;margin-top:0.35rem;line-height:1.5;">{sf["description"]}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
