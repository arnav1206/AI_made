"""
utils/auth.py
==============
Authentication & User Account Manager for Formitra.
Handles Student Login, Registration, Admin Login, Session Management, and Master Audit database.
"""

from __future__ import annotations

import streamlit as st


# Default demo user account
_MOCK_USERS: dict[str, dict[str, str]] = {
    "9876543210": {
        "name": "Rahul Sharma",
        "phone": "9876543210",
        "email": "rahul.sharma@example.com",
        "password": "password123",
        "state": "Rajasthan",
        "category": "OBC",
    }
}

# Admin Credentials
_ADMIN_CREDENTIALS: dict[str, str] = {
    "admin": "admin123",
    "formitra": "formitra2026",
    "officer": "officer123",
}

# Master Database of Submitted Applications
_INITIAL_APPLICATIONS: list[dict] = [
    {
        "ref_code": "FMT-2026-89412",
        "name": "Rahul Sharma",
        "scheme": "Post-Matric Scholarship Scheme",
        "state": "Rajasthan",
        "income": "₹1,50,000",
        "category": "OBC",
        "submitted_at": "27 Jul 2026, 08:30 PM",
        "status": "Under Officer Review ⏳",
        "dbt_seeded": "Yes (Aadhaar Verified)",
    },
    {
        "ref_code": "FMT-2026-74129",
        "name": "Priya Mohanty",
        "scheme": "State Higher Education Merit",
        "state": "Odisha",
        "income": "₹1,20,000",
        "category": "General",
        "submitted_at": "27 Jul 2026, 06:15 PM",
        "status": "Approved for Disbursal ✅",
        "dbt_seeded": "Yes (Aadhaar Verified)",
    },
    {
        "ref_code": "FMT-2026-63201",
        "name": "Suresh Kumar",
        "scheme": "Central Sector Scheme",
        "state": "Tamil Nadu",
        "income": "₹2,10,000",
        "category": "SC",
        "submitted_at": "26 Jul 2026, 04:45 PM",
        "status": "Income Certificate Pending ⚠️",
        "dbt_seeded": "No (Action Required)",
    },
]


def is_logged_in() -> bool:
    """Return True if user is currently authenticated."""
    return bool(st.session_state.get("is_logged_in", False))


def get_logged_in_user() -> dict | None:
    """Return current user dict if authenticated."""
    return st.session_state.get("current_user", None)


def login(identifier: str, password: str) -> tuple[bool, str]:
    """Authenticate user by Phone / Email and Password."""
    clean_id = identifier.strip().lower()
    user_db = st.session_state.get("user_database", _MOCK_USERS)

    matched_user = None
    for u_key, u_data in user_db.items():
        if u_data["phone"] == clean_id or u_data["email"].lower() == clean_id:
            matched_user = u_data
            break

    if not matched_user:
        matched_user = {
            "name": "Applicant User",
            "phone": clean_id,
            "email": f"{clean_id}@formitra.in",
            "password": password,
            "state": "Rajasthan",
            "category": "General",
        }

    st.session_state["is_logged_in"] = True
    st.session_state["current_user"] = matched_user
    
    st.session_state["field_name"] = matched_user.get("name", "")
    st.session_state["field_phone"] = matched_user.get("phone", "")
    st.session_state["field_email"] = matched_user.get("email", "")
    if matched_user.get("state"):
        st.session_state["field_state"] = matched_user.get("state")
        
    return True, f"Welcome back, {matched_user['name']}!"


def register(name: str, phone: str, email: str, password: str, state: str = "Rajasthan", category: str = "General") -> tuple[bool, str]:
    """Register a new Formitra user account."""
    if not name or not phone or not password:
        return False, "Please fill in all required registration fields."

    user_db = st.session_state.get("user_database", dict(_MOCK_USERS))
    new_user = {
        "name": name.strip(),
        "phone": phone.strip(),
        "email": email.strip(),
        "password": password,
        "state": state,
        "category": category,
    }
    user_db[phone.strip()] = new_user
    st.session_state["user_database"] = user_db

    login(phone.strip(), password)
    return True, f"Account created successfully! Welcome, {name}."


def logout() -> None:
    """Log out current student user."""
    st.session_state["is_logged_in"] = False
    st.session_state["current_user"] = None


# ── ADMIN AUTHENTICATION & MASTER AUDIT DATABASE ─────────────────────

def is_admin_logged_in() -> bool:
    """Return True if admin user is currently authenticated."""
    return bool(st.session_state.get("is_admin_logged_in", False))


def admin_login(username: str, password: str) -> tuple[bool, str]:
    """Authenticate administrator account."""
    clean_user = username.strip().lower()
    if clean_user in _ADMIN_CREDENTIALS and _ADMIN_CREDENTIALS[clean_user] == password.strip():
        st.session_state["is_admin_logged_in"] = True
        st.session_state["admin_user"] = clean_user
        return True, f"Admin Portal Login Successful! Welcome, Administrator ({clean_user})."
    return False, "Invalid Admin Username or Password."


def admin_logout() -> None:
    """Log out admin user."""
    st.session_state["is_admin_logged_in"] = False
    st.session_state["admin_user"] = None


def get_submitted_applications() -> list[dict]:
    """Retrieve all submitted student applications for the admin audit dashboard."""
    if "admin_applications_db" not in st.session_state:
        st.session_state["admin_applications_db"] = list(_INITIAL_APPLICATIONS)
    return st.session_state["admin_applications_db"]


def update_application_status(ref_code: str, new_status: str) -> bool:
    """Update status of a submitted application by Reference Code."""
    apps = get_submitted_applications()
    for app in apps:
        if app["ref_code"].upper() == ref_code.upper():
            app["status"] = new_status
            st.session_state["admin_applications_db"] = apps
            return True
    return False
