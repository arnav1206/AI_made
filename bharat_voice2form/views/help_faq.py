"""
views/help_faq.py
==================
Help & FAQ page for Formitra.
Provides step-by-step instructions, voice command guide, and scholarship assistance.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from utils.translations import t
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading("❓ Formitra Help & FAQ Center", "Step-by-step voice form filling guide, scholarship eligibility & support")

    st.markdown(
        '<div class="card" style="border-left:4px solid #FF7A00;">'
        '<div style="font-weight:800;font-size:1.05rem;color:#FF7A00;">🚀 How Formitra Works in 4 Simple Steps</div>'
        '<div style="margin-top:0.75rem;line-height:1.8;font-size:0.92rem;color:#0F172A;">'
        '1️⃣ <b>Select Scheme</b>: Choose your scholarship application (Post-Matric, Central Sector, Pre-Matric, State Merit).<br>'
        '2️⃣ <b>Voice Input</b>: Speak into the mic in your native Indian language (Hindi, Odia, Tamil, Telugu, Bengali, etc.).<br>'
        '3️⃣ <b>AI Auto-Fill</b>: Gemma AI automatically extracts your Name, City, State, Course, Year & Income.<br>'
        '4️⃣ <b>Submit & Track</b>: Review your filled form, download your receipt, and track status with your Reference ID.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown("### ❓ Frequently Asked Questions")

    with st.expander("🗣️ What languages does Formitra support?", expanded=True):
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
