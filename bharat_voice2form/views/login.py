"""
views/login.py
==============
Login page for Formitra.
Supports Mobile / Email password authentication and Reference Number status login.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from utils.translations import t
import utils.auth as auth
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading("🔑 Formitra User Login", "Sign in to access your saved forms, application status & scholarship profile")

    if auth.is_logged_in():
        user = auth.get_logged_in_user()
        name = user.get("name", "Applicant") if user else "Applicant"
        
        st.markdown(
            f'<div class="card" style="border-left:4px solid #059669;background:#ECFDF5;text-align:center;">'
            f'<div style="font-size:2.2rem;margin-bottom:0.4rem;">✅</div>'
            f'<div style="font-size:1.2rem;font-weight:800;color:#065F46;">You are logged in as {name}</div>'
            f'<div style="font-size:0.88rem;color:#047857;margin-top:0.25rem;">'
            f'Mobile: {user.get("phone", "—")} | Email: {user.get("email", "—")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📋 Select Scholarship Scheme →", use_container_width=True, type="primary"):
                session.navigate("form_selection")
        with col2:
            if st.button("🚪 Logout Account", use_container_width=True):
                auth.logout()
                st.toast("Logged out successfully.")
                st.rerun()

        return

    # Login Container Box
    c1, c2, c3 = st.columns([1, 2.2, 1])
    with c2:
        st.markdown(
            '<div class="card" style="border-top:4px solid #FF7A00;text-align:center;">'
            '<div style="font-size:2.2rem;margin-bottom:0.3rem;">🎙️</div>'
            '<div style="font-size:1.2rem;font-weight:900;color:#FF7A00;">Formitra Portal Login</div>'
            '<div style="font-size:0.85rem;opacity:0.8;margin-top:0.2rem;">'
            'Enter your registered Mobile Number / Email to continue.</div>'
            '</div>',
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.tabs(["📱 Password / OTP Login", "🔍 Track Reference Code"])

        with tab1:
            identifier = st.text_input(
                "Mobile Number / Email Address",
                value="9876543210",
                placeholder="e.g. 9876543210 or rahul@example.com",
                key="login_identifier",
            )
            password = st.text_input(
                "Password",
                value="password123",
                type="password",
                placeholder="Enter your account password",
                key="login_password",
            )

            if st.button("🔐 Login to Account", use_container_width=True, type="primary"):
                if identifier.strip() and password.strip():
                    success, msg = auth.login(identifier, password)
                    if success:
                        st.toast(msg)
                        session.navigate("form_selection")
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter your mobile number and password.")

        with tab2:
            ref_code = st.text_input(
                "Formitra Reference Code",
                placeholder="e.g. FMT-2026-89412",
                key="login_ref_code",
            )
            if st.button("🔎 Login via Reference Code", use_container_width=True):
                if ref_code.strip():
                    session.set("active_ref_code", ref_code.strip().upper())
                    session.navigate("track_status")
                else:
                    st.warning("Please enter your reference code.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div style="text-align:center;font-size:0.9rem;">'
            'Don\'t have a Formitra account yet?'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("📝 Create New Account (Register) →", use_container_width=True):
            session.navigate("register")

    spacer()
    info_box("💡 Note: Registering an account auto-saves your profile details for instant voice form auto-filling.")
