"""
utils/session.py
================
Centralised session-state management for Bharat Voice2Form / Formitra.
"""

from __future__ import annotations

import streamlit as st
from utils.constants import (
    PAGE_HOME,
    PAGE_ORDER,
    APPLICATION_NUMBER,
    ALL_FIELD_NAMES,
)


_DEFAULTS: dict = {
    "page":               "login",
    "selected_form":      "",
    "selected_language":  "Hindi",
    "is_recording":       False,
    "transcript":         "",
    "extracted_data":     {},
    "extraction_done":    False,
    "form_data":          {},
    "application_no":     "",
    "declaration_agreed": False,
}


def init() -> None:
    """Initialise all session-state keys with their defaults."""
    for key, default in _DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


def navigate(page: str) -> None:
    """Set the active page and trigger a rerun."""
    if page not in PAGE_ORDER:
        raise ValueError(f"Unknown page key: '{page}'.")
    st.session_state.page = page
    st.rerun()


def get(key: str, default=None):
    """Safely read a session-state key."""
    return st.session_state.get(key, default)


def set(key: str, value) -> None:  # noqa: A001
    """Write to session state."""
    st.session_state[key] = value


def reset_recording() -> None:
    """Clear microphone / transcript state before a new recording session."""
    st.session_state.is_recording = False
    st.session_state.transcript   = ""


def reset_extraction() -> None:
    """Clear AI extraction results AND cached widget values so new dictation fills the form."""
    st.session_state.extracted_data  = {}
    st.session_state.extraction_done = False
    reset_form_fields()


def reset_form_fields() -> None:
    """Clear all individual form field values (field_* keys)."""
    for key in list(st.session_state.keys()):
        if key.startswith("field_"):
            del st.session_state[key]


def save_form_data() -> dict:
    """
    Collect all field_* keys from session state into a structured dict.
    """
    mapping = {
        "Full Name":            "field_name",
        "Date of Birth":        "field_dob",
        "Gender":               "field_gender",
        "Category":             "field_category",
        "Address":              "field_address",
        "City":                 "field_city",
        "State":                "field_state",
        "PIN Code":             "field_pin",
        "College":              "field_college",
        "Course":               "field_course",
        "Year":                 "field_year",
        "Annual Family Income": "field_income",
        "Phone Number":         "field_phone",
        "Email":                "field_email",
        "Percentage / CGPA":    "field_percentage",
    }
    form_data = {
        label: st.session_state.get(key, "")
        for label, key in mapping.items()
    }
    st.session_state.form_data = form_data
    return form_data


def full_reset() -> None:
    """Hard-reset all transient state except the page key."""
    transient_keys = [
        "selected_form", "selected_language", "is_recording",
        "transcript", "extracted_data", "extraction_done",
        "form_data", "application_no", "declaration_agreed",
    ]
    for key in transient_keys:
        st.session_state.pop(key, None)
    reset_form_fields()

    for key in transient_keys:
        st.session_state[key] = _DEFAULTS.get(key, None)


def generate_application_number() -> str:
    """Return (and persist) a mock application reference number."""
    if not st.session_state.get("application_no"):
        st.session_state.application_no = APPLICATION_NUMBER
    return st.session_state.application_no
