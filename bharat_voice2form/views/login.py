"""
views/login.py
==============
Initial Login & Authentication Page for Formitra.
100% Multilingual translation support via t().
Supports Password/OTP authentication, Reference Number tracking, Guest mode & New Registration.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from utils.translations import t
import utils.auth as auth
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading(t("login_heading"), t("login_sub"))

    if auth.is_logged_in():
        user = auth.get_logged_in_user()
        name = user.get("name", "Applicant") if user else "Applicant"
        
        st.markdown(
            f'<div class="card" style="border-left:5px solid #059669;background:linear-gradient(135deg, #ECFDF5, #D1FAE5);text-align:center;padding:2rem;">'
            f'<div style="font-size:3rem;margin-bottom:0.5rem;">🎉</div>'
            f'<div style="font-size:1.4rem;font-weight:900;color:#065F46;">Authenticated as {name}</div>'
            f'<div style="font-size:0.92rem;color:#047857;margin-top:0.35rem;">'
            f'Mobile: <b>{user.get("phone", "—")}</b> | Email: <b>{user.get("email", "—")}</b></div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f'📋 {t("select_form")} →', use_container_width=True, type="primary"):
                session.navigate("form_selection")
        with col2:
            if st.button("🚪 Logout Account", use_container_width=True):
                auth.logout()
                st.toast("Logged out successfully.")
                st.rerun()

        return

    # Login Container Box
    c1, c2, c3 = st.columns([1, 2.4, 1])
    with c2:
        st.markdown(
            f'<div class="card" style="border-top:5px solid #FF7A00;text-align:center;padding:2rem 1.5rem;">'
            f'<div style="font-size:2.8rem;margin-bottom:0.4rem;">🎙️</div>'
            f'<div style="font-size:1.35rem;font-weight:900;color:#FF7A00;">{t("login_card_title")}</div>'
            f'<div style="font-size:0.88rem;opacity:0.85;margin-top:0.3rem;line-height:1.5;">'
            f'{t("login_card_sub")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        tab1, tab2, tab3 = st.tabs([t("login_tab_pwd"), t("login_tab_demo"), t("login_tab_ref")])

        with tab1:
            identifier = st.text_input(
                t("login_id_label"),
                value="9876543210",
                placeholder="e.g. 9876543210 or rahul@example.com",
                key="login_identifier",
            )
            password = st.text_input(
                t("login_pwd_label"),
                value="password123",
                type="password",
                placeholder="Enter your account password",
                key="login_password",
            )

            if st.button(t("login_submit_btn"), use_container_width=True, type="primary"):
                if identifier.strip() and password.strip():
                    success, msg = auth.login(identifier, password)
                    if success:
                        st.toast(msg)
                        session.navigate("home")
                    else:
                        st.error(msg)
                else:
                    st.warning("Please enter your mobile number and password.")

        with tab2:
            st.markdown(
                '<div style="font-size:0.88rem;opacity:0.85;margin:0.5rem 0 1rem;line-height:1.5;text-align:center;">'
                'Testing the platform? Login immediately using the default <b>Rahul Sharma (Demo Profile)</b> account.'
                '</div>',
                unsafe_allow_html=True,
            )
            if st.button(t("login_demo_btn"), use_container_width=True, type="primary"):
                auth.login("9876543210", "password123")
                st.toast("Logged in as Rahul Sharma (Demo Account)")
                session.navigate("home")

        with tab3:
            ref_code = st.text_input(
                t("app_number"),
                placeholder="e.g. FMT-2026-89412",
                key="login_ref_code",
            )
            if st.button("🔎 Access via Reference Code", use_container_width=True):
                if ref_code.strip():
                    session.set("active_ref_code", ref_code.strip().upper())
                    session.navigate("track_status")
                else:
                    st.warning("Please enter your reference code.")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:center;font-size:0.9rem;">'
            f'{t("login_no_acct")}'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("login_create_acct"), use_container_width=True):
            session.navigate("register")

    spacer()
    info_box("💡 Note: Authenticating your account links your profile, speech recordings, and verified scholarship documents across sessions.")
