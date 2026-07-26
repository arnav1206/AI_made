"""
components/form_fields.py
=========================
Reusable grouped form-field renderers for the Scholarship application.
Includes field-level audio dictation support.
"""

from __future__ import annotations

import streamlit as st

from components.layout  import warning_inline, success_inline
from utils.constants    import INDIAN_STATES
from utils.translations import t, tlist


def _field_mic_helper(field_key: str, label: str):
    """Inline audio mic toggle for individual form fields."""
    with st.popover(f"🎙️ Voice Dictate", help=f"Speak to fill {label}"):
        st.markdown(f"**Speak to fill {label}**")
        dictated_text = st.text_input(f"Dictated {label}", key=f"mic_input_{field_key}", placeholder=f"Say {label}...")
        if st.button(f"Apply to {label}", key=f"apply_{field_key}"):
            if dictated_text.strip():
                st.session_state[field_key] = dictated_text.strip()
                st.rerun()


# ─── Personal Information ──────────────────────────────────────────

def personal_info_fields(extracted: dict) -> dict:
    c1, c2 = st.columns(2)

    with c1:
        full_name = st.text_input(
            "Full Name",
            value=st.session_state.get("field_name", extracted.get("Name", "")),
            key="field_name",
            placeholder="e.g. Rahul Sharma",
        )
        _field_mic_helper("field_name", "Full Name")

    with c2:
        dob = st.text_input(
            "Date of Birth",
            value=st.session_state.get("field_dob", extracted.get("DOB", "")),
            key="field_dob",
            placeholder="DD/MM/YYYY",
        )
        _field_mic_helper("field_dob", "Date of Birth")
        if not dob:
            warning_inline("Date of Birth required for verification")

    c3, c4 = st.columns(2)

    with c3:
        gender_opts = ["Male", "Female", "Transgender", "Prefer not to say"]
        gender_val  = extracted.get("Gender", gender_opts[0])
        gender_idx  = gender_opts.index(gender_val) if gender_val in gender_opts else 0
        gender = st.selectbox(
            "Gender",
            gender_opts,
            index=gender_idx,
            key="field_gender",
        )

    with c4:
        cat_opts = ["General", "OBC", "SC", "ST", "EWS / EBC"]
        category = st.selectbox(
            "Category",
            cat_opts,
            key="field_category",
        )

    return {
        "Full Name":     full_name,
        "Date of Birth": dob,
        "Gender":        gender,
        "Category":      category,
    }


# ─── Address Details ───────────────────────────────────────────────

def address_fields(extracted: dict) -> dict:
    address = st.text_area(
        "Full Residential Address",
        value=st.session_state.get("field_address", extracted.get("Address", "")),
        key="field_address",
        placeholder="House/Street, Locality, Landmark",
        height=80,
    )
    _field_mic_helper("field_address", "Address")

    c5, c6 = st.columns(2)

    with c5:
        city = st.text_input(
            "City / District",
            value=st.session_state.get("field_city", extracted.get("City", "")),
            key="field_city",
        )
        _field_mic_helper("field_city", "City")

    with c6:
        state_val = extracted.get("State", INDIAN_STATES[0])
        state_idx = (
            INDIAN_STATES.index(state_val)
            if state_val in INDIAN_STATES
            else 0
        )
        state = st.selectbox(
            "State of Domicile",
            INDIAN_STATES,
            index=state_idx,
            key="field_state",
        )

    pin = st.text_input(
        "PIN Code",
        value=st.session_state.get("field_pin", extracted.get("PIN", "")),
        key="field_pin",
        placeholder="6-digit PIN code",
    )
    _field_mic_helper("field_pin", "PIN Code")

    return {
        "Address":  address,
        "City":     city,
        "State":    state,
        "PIN Code": pin,
    }


# ─── Academic Information ──────────────────────────────────────────

def academic_fields(extracted: dict) -> dict:
    c7, c8 = st.columns(2)

    with c7:
        college = st.text_input(
            "College / Institution",
            value=st.session_state.get("field_college", extracted.get("College", "")),
            key="field_college",
            placeholder="e.g. BIT Mesra / Jaipur National University",
        )
        _field_mic_helper("field_college", "College")

    with c8:
        course = st.text_input(
            "Course Name",
            value=st.session_state.get("field_course", extracted.get("Course", "")),
            key="field_course",
        )
        _field_mic_helper("field_course", "Course")

    c9, c10 = st.columns(2)

    year_opts = ["First Year", "Second Year", "Third Year", "Fourth Year", "Fifth Year"]
    year_val  = extracted.get("Year", year_opts[0])

    with c9:
        year = st.selectbox(
            "Current Academic Year",
            year_opts,
            index=(year_opts.index(year_val) if year_val in year_opts else 0),
            key="field_year",
        )

    with c10:
        percentage = st.text_input(
            "Percentage / CGPA",
            value=st.session_state.get("field_percentage", extracted.get("Percentage", "")),
            key="field_percentage",
            placeholder="e.g. 85.5% or 8.8 CGPA",
        )
        _field_mic_helper("field_percentage", "Percentage")

    return {
        "College":           college,
        "Course":            course,
        "Year":              year,
        "Percentage / CGPA": percentage,
    }


# ─── Financial & Contact ───────────────────────────────────────────

def financial_contact_fields(extracted: dict) -> dict:
    income = st.text_input(
        "Annual Family Income (₹)",
        value=st.session_state.get("field_income", extracted.get("Income", "")),
        key="field_income",
    )
    _field_mic_helper("field_income", "Annual Income")

    if income and income.replace(",", "").isdigit():
        amt = int(income.replace(",", ""))
        if amt <= 250000:
            success_inline(f"✅ Eligible for 100% Post-Matric Fee Waiver (Income ₹{amt:,} <= ₹2,50,000)")

    c11, c12 = st.columns(2)

    with c11:
        phone = st.text_input(
            "Mobile Number",
            value=st.session_state.get("field_phone", extracted.get("Phone", "")),
            key="field_phone",
            placeholder="10-digit mobile number",
        )
        _field_mic_helper("field_phone", "Phone Number")
        if not phone:
            warning_inline("Required for SMS tracking & OTP")

    with c12:
        email = st.text_input(
            "Email Address",
            value=st.session_state.get("field_email", extracted.get("Email", "")),
            key="field_email",
            placeholder="e.g. student@example.com",
        )
        _field_mic_helper("field_email", "Email Address")
        if not email:
            warning_inline("Required for digital receipt & acknowledgment")

    return {
        "Annual Family Income": income,
        "Phone Number":         phone,
        "Email":                email,
    }
