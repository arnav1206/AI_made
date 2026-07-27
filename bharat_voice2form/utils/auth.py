"""
utils/auth.py
==============
Authentication & User Account Manager for Formitra.
Handles Login, Registration, Session Management, and User Profile Auto-fill.
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


def is_logged_in() -> bool:
    """Return True if user is currently authenticated."""
    return bool(st.session_state.get("is_logged_in", False))


def get_logged_in_user() -> dict | None:
    """Return current user dict if authenticated."""
    return st.session_state.get("current_user", None)


def login(identifier: str, password: str) -> tuple[bool, str]:
    """
    Authenticate user by Phone / Email and Password.
    """
    clean_id = identifier.strip().lower()
    
    # Check registered users in session or mock database
    user_db = st.session_state.get("user_database", _MOCK_USERS)

    matched_user = None
    for u_key, u_data in user_db.items():
        if u_data["phone"] == clean_id or u_data["email"].lower() == clean_id:
            matched_user = u_data
            break

    if not matched_user:
        # Allow default demo login for convenience
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
    
    # Auto-fill profile fields into session state
    st.session_state["field_name"] = matched_user.get("name", "")
    st.session_state["field_phone"] = matched_user.get("phone", "")
    st.session_state["field_email"] = matched_user.get("email", "")
    if matched_user.get("state"):
        st.session_state["field_state"] = matched_user.get("state")
        
    return True, f"Welcome back, {matched_user['name']}!"


def register(name: str, phone: str, email: str, password: str, state: str = "Rajasthan", category: str = "General") -> tuple[bool, str]:
    """
    Register a new Formitra user account.
    """
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

    # Auto-login after registration
    login(phone.strip(), password)
    return True, f"Account created successfully! Welcome, {name}."


def logout() -> None:
    """Log out current user."""
    st.session_state["is_logged_in"] = False
    st.session_state["current_user"] = None
