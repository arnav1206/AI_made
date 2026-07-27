"""
views/help_faq.py
==================
Help & FAQ page for Formitra.
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

    section_heading("❓ Formitra Help & FAQ Center", "Step-by-step voice form filling guide, Chrome Extension setup & support")

    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        step_hdr = "#FF7A00"
        step_txt = "#F8FAFC"
    else:
        step_hdr = "#C2410C"
        step_txt = "#1E293B"

    st.markdown(
        f'<div class="card" style="border-left:4px solid #FF7A00;">'
        f'<div style="font-weight:800;font-size:1.05rem;color:{step_hdr};">🚀 How Formitra Works in 4 Simple Steps</div>'
        f'<div style="margin-top:0.75rem;line-height:1.8;font-size:0.92rem;color:{step_txt};">'
        f'1️⃣ <b>Select Scheme</b>: Choose your scholarship application (Post-Matric, Central Sector, Pre-Matric, State Merit).<br>'
        f'2️⃣ <b>Voice Input</b>: Speak into the mic in your native Indian language (Hindi, Odia, Tamil, Telugu, Bengali, etc.).<br>'
        f'3️⃣ <b>AI Auto-Fill</b>: Gemma AI automatically extracts your Name, City, State, Course, Year & Income.<br>'
        f'4️⃣ <b>Submit & Track</b>: Review your filled form, download your receipt, and track status with your Reference ID.'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("🧩 How do I install the standalone Formitra Chrome Browser Extension?", expanded=True):
        st.markdown(
            "Formitra is available as a standalone **Google Chrome Browser Extension (Manifest V3)** that allows you to auto-fill forms on ANY web page!\n\n"
            "**Installation Steps:**\n"
            "1. Open Chrome and go to `chrome://extensions/`\n"
            "2. Turn **ON** 'Developer mode' in the top-right corner.\n"
            "3. Click **'Load unpacked'** and select the `formitra_chrome_extension/` directory.\n"
            "4. Open any web form, click the Formitra mic icon, and speak to auto-fill!"
        )

    with st.expander("🗣️ What languages does Formitra support?"):
        st.write(
            "Formitra supports 9 official Indian languages: Hindi (हिन्दी), Odia (ଓଡ଼ିଆ), Tamil (தமிழ்), "
            "Telugu (తెలుగు), Bengali (বাংলা), Marathi (मराठी), Kannada (ಕನ್ನಡ), Malayalam (മലയാളം), and English."
        )

    with st.expander("🎙️ How do I use field-level voice dictation on individual form inputs?"):
        st.write(
            "On the 'Form Review' page, click the mic 🎙️ icon next to any input box. Speak into your microphone, "
            "and Formitra will type your spoken text directly into that specific input field!"
        )

    with st.expander("📄 What documents do I need for Scholarship registration?"):
        st.write(
            "• Aadhaar Card\n"
            "• Previous Academic Marksheets\n"
            "• Annual Family Income Certificate (Issued by Tehsildar/SDO)\n"
            "• Caste/Category Certificate (if applicable)\n"
            "• Bank Passbook (Aadhaar seeded account)"
        )

    with st.expander("🔍 How do I track my submitted scholarship application?"):
        st.write(
            "Go to the 'Track / Login' tab from the sidebar menu, enter your 10-character Reference Code (e.g. FMT-2026-89412), "
            "and view your application verification status and submitted PDF receipt."
        )

    spacer()
    info_box("📞 Need further assistance? Contact Formitra National Toll-Free Helpline: 1800-111-2026 (Mon-Sat 9 AM - 6 PM)")
