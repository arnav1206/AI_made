"""
components/form_fields.py
=========================
Reusable grouped form-field renderers for the Scholarship application.
100% Multilingual translation support via t().
Includes field-level live audio dictation & text dictation support with canonical Streamlit state binding.
"""

from __future__ import annotations

import hashlib
import streamlit as st

from components.layout  import warning_inline, success_inline
from utils.constants    import INDIAN_STATES
from utils.translations import t, tlist
from utils.speech_to_text import transcribe


def _field_mic_helper(field_key: str, label: str):
    """Inline audio mic toggle for individual form fields with live audio & text dictation."""
    dictate_btn_lbl = t("btn_voice_dictate", "🎙️ Voice Dictate")
    with st.popover(dictate_btn_lbl, help=f"Speak to fill {label}"):
        st.markdown(f"### 🎙️ Dictate {label}")
        st.markdown(f"<div style='font-size:0.83rem;opacity:0.85;margin-bottom:0.5rem;'>Record an audio clip or type to update <b>{label}</b> directly:</div>", unsafe_allow_html=True)
        
        # 1. Direct Microphone Audio Clip Recording
        audio_val = st.audio_input(f"Record audio for {label}", key=f"audio_mic_{field_key}")
        if audio_val is not None:
            audio_bytes = audio_val.read()
            audio_hash  = hashlib.md5(audio_bytes).hexdigest()
            if st.session_state.get(f"last_hash_{field_key}") != audio_hash:
                st.session_state[f"last_hash_{field_key}"] = audio_hash
                lang = st.session_state.get("selected_language", "Hindi")
                with st.spinner(f"🎙️ Transcribing {label} in {lang}…"):
                    res = transcribe(audio_bytes=audio_bytes, language=lang)
                if res and res.text and res.text.strip():
                    st.session_state[field_key] = res.text.strip()
                    st.toast(f"✅ {label} updated to: {res.text.strip()}")
                    st.rerun()

        st.markdown("<hr style='margin:0.5rem 0;opacity:0.2;'>", unsafe_allow_html=True)

        # 2. Text / Speech Edit Dictation Input
        dictated_text = st.text_input(
            f"Dictated {label}",
            key=f"mic_input_{field_key}",
            placeholder=f"Say {label}...",
        )
        if st.button(f"🚀 Apply to {label}", key=f"apply_{field_key}", type="primary"):
            if dictated_text.strip():
                st.session_state[field_key] = dictated_text.strip()
                st.toast(f"✅ {label} updated!")
                st.rerun()


# ─── Personal Information ──────────────────────────────────────────

def personal_info_fields(extracted: dict) -> dict:
    if "field_name" not in st.session_state:
        st.session_state["field_name"] = extracted.get("Name", "")
    if "field_dob" not in st.session_state:
        st.session_state["field_dob"] = extracted.get("DOB", "")

    c1, c2 = st.columns(2)

    with c1:
        full_name = st.text_input(
            t("reg_name", "Full Name"),
            key="field_name",
            placeholder="e.g. Rahul Sharma",
        )
        _field_mic_helper("field_name", t("reg_name", "Full Name"))

    with c2:
        dob = st.text_input(
            t("lbl_dob", "Date of Birth"),
            key="field_dob",
            placeholder="DD/MM/YYYY",
        )
        if not dob:
            warning_inline("Date of Birth required for verification")
        _field_mic_helper("field_dob", t("lbl_dob", "Date of Birth"))

    c3, c4 = st.columns(2)

    with c3:
        gender_opts = ["— Select —", "Male", "Female", "Transgender", "Prefer not to say"]
        gender_val  = extracted.get("Gender", gender_opts[0])
        if "field_gender" not in st.session_state:
            st.session_state["field_gender"] = gender_val if gender_val in gender_opts else gender_opts[0]
        
        gender = st.selectbox(
            t("lbl_gender", "Gender"),
            gender_opts,
            key="field_gender",
        )

    with c4:
        cat_opts = ["— Select —", "General", "OBC", "SC", "ST", "EWS / EBC"]
        cat_val  = extracted.get("Category", cat_opts[0])
        if "field_category" not in st.session_state:
            st.session_state["field_category"] = cat_val if cat_val in cat_opts else cat_opts[0]

        category = st.selectbox(
            t("reg_category", "Category"),
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
    if "field_address" not in st.session_state:
        st.session_state["field_address"] = extracted.get("Address", "")
    if "field_city" not in st.session_state:
        st.session_state["field_city"] = extracted.get("City", "")
    if "field_pin" not in st.session_state:
        st.session_state["field_pin"] = extracted.get("PIN", "")

    address = st.text_area(
        t("lbl_address", "Full Residential Address"),
        key="field_address",
        placeholder="House/Street, Locality, Landmark",
        height=80,
    )
    _field_mic_helper("field_address", t("lbl_address", "Address"))

    c5, c6 = st.columns(2)

    with c5:
        city = st.text_input(
            t("lbl_city", "City / District"),
            key="field_city",
        )
        _field_mic_helper("field_city", t("lbl_city", "City"))

    with c6:
        state_val = extracted.get("State", INDIAN_STATES[0])
        if "field_state" not in st.session_state:
            st.session_state["field_state"] = state_val if state_val in INDIAN_STATES else INDIAN_STATES[0]

        state = st.selectbox(
            t("reg_state", "State of Domicile"),
            INDIAN_STATES,
            key="field_state",
        )

    pin = st.text_input(
        t("lbl_pin", "PIN Code"),
        key="field_pin",
        placeholder="6-digit PIN code",
    )
    _field_mic_helper("field_pin", t("lbl_pin", "PIN Code"))

    return {
        "Address":  address,
        "City":     city,
        "State":    state,
        "PIN Code": pin,
    }


# ─── Academic Information ──────────────────────────────────────────

def academic_fields(extracted: dict) -> dict:
    if "field_college" not in st.session_state:
        st.session_state["field_college"] = extracted.get("College", "")
    if "field_course" not in st.session_state:
        st.session_state["field_course"] = extracted.get("Course", "")
    if "field_percentage" not in st.session_state:
        st.session_state["field_percentage"] = extracted.get("Percentage", "")

    c7, c8 = st.columns(2)

    with c7:
        college = st.text_input(
            t("lbl_college", "College / Institution"),
            key="field_college",
            placeholder="e.g. BIT Mesra / Jaipur National University",
        )
        _field_mic_helper("field_college", t("lbl_college", "College"))

    with c8:
        course = st.text_input(
            t("lbl_course", "Course Name"),
            key="field_course",
        )
        _field_mic_helper("field_course", t("lbl_course", "Course"))

    c9, c10 = st.columns(2)

    year_opts = ["— Select —", "First Year", "Second Year", "Third Year", "Fourth Year", "Fifth Year"]
    year_val  = extracted.get("Year", year_opts[0])
    if "field_year" not in st.session_state:
        st.session_state["field_year"] = year_val if year_val in year_opts else year_opts[0]

    with c9:
        year = st.selectbox(
            t("lbl_year", "Current Academic Year"),
            year_opts,
            key="field_year",
        )

    with c10:
        percentage = st.text_input(
            t("lbl_percentage", "Percentage / CGPA"),
            key="field_percentage",
            placeholder="e.g. 85.5% or 8.8 CGPA",
        )
        _field_mic_helper("field_percentage", t("lbl_percentage", "Percentage"))

    return {
        "College":           college,
        "Course":            course,
        "Year":              year,
        "Percentage / CGPA": percentage,
    }


# ─── Financial & Contact ───────────────────────────────────────────

def financial_contact_fields(extracted: dict) -> dict:
    if "field_income" not in st.session_state:
        st.session_state["field_income"] = extracted.get("Income", "")
    if "field_phone" not in st.session_state:
        st.session_state["field_phone"] = extracted.get("Phone", "")
    if "field_email" not in st.session_state:
        st.session_state["field_email"] = extracted.get("Email", "")

    income = st.text_input(
        t("lbl_income", "Annual Family Income (₹)"),
        key="field_income",
        placeholder="e.g. 150000",
    )
    _field_mic_helper("field_income", t("lbl_income", "Income"))

    c11, c12 = st.columns(2)

    with c11:
        phone = st.text_input(
            t("reg_phone", "Mobile Number"),
            key="field_phone",
            placeholder="10-digit mobile number",
        )
        _field_mic_helper("field_phone", t("reg_phone", "Mobile Number"))

    with c12:
        email = st.text_input(
            t("reg_email", "Email Address"),
            key="field_email",
            placeholder="e.g. applicant@example.com",
        )
        _field_mic_helper("field_email", t("reg_email", "Email Address"))

    return {
        "Annual Family Income": income,
        "Phone Number":         phone,
        "Email":                email,
    }
