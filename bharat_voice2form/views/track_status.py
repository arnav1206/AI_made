"""
views/track_status.py
======================
Reference Number Login & Application Tracker Page for Formitra.
Allows users to enter their tracking code (e.g. FMT-2026-89412) to view application status, details, and download PDF receipt.
Dynamic Light/Dark mode contrast support.
"""

from __future__ import annotations

import streamlit as st

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.translations  import t
from utils.pdf_generator import generate as generate_pdf
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading("🔍 Track Application Status / Login", "Enter your Formitra Reference Number to check application status")

    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        card_title  = "#F8FAFC"
        card_sub    = "#CBD5E1"
        profile_hdr = "#34D399"
        txt_main    = "#F8FAFC"
        hr_border   = "rgba(255, 255, 255, 0.15)"
    else:
        card_title  = "#0F172A"
        card_sub    = "#64748B"
        profile_hdr = "#065F46"
        txt_main    = "#0F172A"
        hr_border   = "#E2E8F0"

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(
            f'<div class="card" style="border-top:4px solid #FF7A00;text-align:center;">'
            f'<div style="font-size:2rem;margin-bottom:0.5rem;">🔑</div>'
            f'<div style="font-size:1.1rem;font-weight:800;color:{card_title};">Applicant Reference Login</div>'
            f'<div style="font-size:0.85rem;color:{card_sub};margin-top:0.25rem;">'
            f'Enter the unique reference code provided upon submitting your scholarship form.</div>'
            f'</div>',
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
    st.markdown(f"<hr style='border:none;border-top:1px solid {hr_border};margin:2rem 0;'>", unsafe_allow_html=True)

    if active_ref:
        st.markdown(f"### 📋 Application Details for Reference: `{active_ref}`")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Application Status", "✅ Verified & Submitted")
        with col2:
            st.metric("Scheme Portal", session.get("selected_form") or "Post-Matric Scholarship")
        with col3:
            st.metric("Verification Level", "Level 1 (Institute Level)")

        st.markdown("<br>", unsafe_allow_html=True)

        extracted = session.get("extracted_data", {})
        form_data = session.get("form_data", {})
        name   = extracted.get("Name")   or session.get("field_name")   or "Rahul Sharma"
        state  = extracted.get("State")  or session.get("field_state")  or "Rajasthan"
        city   = extracted.get("City")   or session.get("field_city")   or "Jaipur"
        course = extracted.get("Course") or session.get("field_course") or "B.Tech"
        year   = extracted.get("Year")   or session.get("field_year")   or "Second Year"
        income = extracted.get("Income") or session.get("field_income") or "150000"

        st.markdown(
            f'<div class="card" style="border-left:4px solid #059669;">'
            f'<div style="font-weight:800;font-size:1.05rem;color:{profile_hdr};margin-bottom:0.75rem;">'
            f'👤 Submitted Applicant Profile</div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:0.75rem;font-size:0.9rem;color:{txt_main};">'
            f'<div><b>Applicant Name:</b> {name}</div>'
            f'<div><b>State:</b> {state}</div>'
            f'<div><b>City:</b> {city}</div>'
            f'<div><b>Course & Year:</b> {course} ({year})</div>'
            f'<div><b>Family Income:</b> ₹{income}</div>'
            f'<div><b>Submission Date:</b> 26 July 2026</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        # PDF Receipt Download on Track Status Page
        pdf_res = generate_pdf(
            form_data=form_data if form_data else {
                "Full Name": name,
                "State": state,
                "City": city,
                "Course": course,
                "Year": year,
                "Annual Family Income": f"₹{income}",
            },
            application_no=active_ref,
            form_title=session.get("selected_form") or "Post-Matric Scholarship Scheme",
        )
        if pdf_res:
            st.download_button(
                label="📄 Download Official Submitted Application PDF",
                data=pdf_res.pdf_bytes,
                file_name=pdf_res.filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )

        spacer(0.5)
        info_box("💡 Note: Official updates regarding your scholarship disbursement will be sent via SMS to your registered mobile number.")
