"""
views/track_status.py
======================
Reference Number Login & Application Tracker Page for Formitra.
Allows users to enter their tracking code (e.g. FMT-2026-89412) to view application status and PDF details.
"""

from __future__ import annotations

import streamlit as st

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.translations  import t
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading("🔍 Track Application Status / Login", "Enter your Formitra Reference Number to check application status")

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            '<div class="card" style="border-top:4px solid #FF7A00;text-align:center;">'
            '<div style="font-size:2rem;margin-bottom:0.5rem;">🔑</div>'
            '<div style="font-size:1.1rem;font-weight:800;color:#0F172A;">Applicant Reference Login</div>'
            '<div style="font-size:0.85rem;color:#64748B;margin-top:0.25rem;">'
            'Enter the unique reference code provided upon submitting your scholarship form.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        ref_input = st.text_input(
            "Formitra Reference Number",
            value=session.get("active_ref_code", "FMT-2026-89412"),
            placeholder="e.g. FMT-2026-89412",
            key="ref_input_code",
        )

        if st.button("🔎 Track Application Status", use_container_width=True, type="primary"):
            session.set("active_ref_code", ref_input.strip().upper())
            st.rerun()

    active_ref = session.get("active_ref_code", "FMT-2026-89412")
    st.markdown("<hr style='border:none;border-top:1px solid #E2E8F0;margin:2rem 0;'>", unsafe_allow_html=True)

    if active_ref:
        st.markdown(f"### 📋 Application Details for Reference: `{active_ref}`")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Application Status", "✅ Verified & Submitted")
        with col2:
            st.metric("Scheme Portal", session.get("selected_form", "Post-Matric Scholarship"))
        with col3:
            st.metric("Verification Level", "Level 1 (Institute Level)")

        st.markdown("<br>", unsafe_allow_html=True)

        extracted = session.get("extracted_data", {
            "Name": "Rahul Sharma",
            "City": "Jaipur",
            "State": "Rajasthan",
            "Course": "B.Tech",
            "Year": "Second Year",
            "Income": "150000",
        })

        st.markdown(
            f'<div class="card" style="border-left:4px solid #059669;">'
            f'<div style="font-weight:800;font-size:1rem;color:#065F46;margin-bottom:0.75rem;">'
            f'👤 Submitted Applicant Profile</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;font-size:0.9rem;">'
            f'<div><b>Applicant Name:</b> {extracted.get("Name", "Rahul Sharma")}</div>'
            f'<div><b>State:</b> {extracted.get("State", "Rajasthan")}</div>'
            f'<div><b>City:</b> {extracted.get("City", "Jaipur")}</div>'
            f'<div><b>Course & Year:</b> {extracted.get("Course", "B.Tech")} ({extracted.get("Year", "Second Year")})</div>'
            f'<div><b>Family Income:</b> ₹{extracted.get("Income", "150000")}</div>'
            f'<div><b>Submission Date:</b> 26 July 2026</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        info_box("💡 Note: Official updates regarding your scholarship disbursement will be sent via SMS to your registered mobile number.")
