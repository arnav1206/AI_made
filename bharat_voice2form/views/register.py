"""
views/register.py
=================
Registration / Account Creation Page for Formitra.
100% Multilingual translation support via t().
Allows new applicants to create an account profile.
"""

from __future__ import annotations

import streamlit as st

from components.layout import tricolour_bar, section_heading, info_box, spacer
from utils.constants   import INDIAN_STATES
from utils.translations import t
import utils.auth as auth
import utils.session as session


def render() -> None:
    tricolour_bar()

    section_heading(t("reg_heading"), t("reg_sub"))

    c1, c2, c3 = st.columns([1, 2.4, 1])
    with c2:
        st.markdown(
            f'<div class="card" style="border-top:4px solid #138808;text-align:center;">'
            f'<div style="font-size:2.2rem;margin-bottom:0.3rem;">📋</div>'
            f'<div style="font-size:1.2rem;font-weight:900;color:#138808;">{t("reg_card_title")}</div>'
            f'<div style="font-size:0.85rem;opacity:0.8;margin-top:0.2rem;">'
            f'{t("reg_card_sub")}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        name = st.text_input(
            t("reg_name"),
            placeholder="e.g. Rahul Sharma",
            key="reg_name",
        )

        col_p, col_e = st.columns(2)
        with col_p:
            phone = st.text_input(
                t("reg_phone"),
                placeholder="10-digit mobile number",
                key="reg_phone",
            )
        with col_e:
            email = st.text_input(
                t("reg_email"),
                placeholder="e.g. rahul@example.com",
                key="reg_email",
            )

        col_s, col_c = st.columns(2)
        with col_s:
            state = st.selectbox(
                t("reg_state"),
                INDIAN_STATES,
                index=0, # Default to "-- Select --"
                key="reg_state",
            )
        with col_c:
            category = st.selectbox(
                t("reg_category"),
                ["— Select —", "General", "OBC", "SC", "ST", "EWS / EBC"],
                index=0, # Default to "-- Select --"
                key="reg_category",
            )

        pass1 = st.text_input(
            t("reg_pass1"),
            type="password",
            placeholder="At least 6 characters",
            key="reg_pass1",
        )
        pass2 = st.text_input(
            t("reg_pass2"),
            type="password",
            placeholder="Re-enter password",
            key="reg_pass2",
        )

        if st.button(t("reg_submit"), use_container_width=True, type="primary"):
            if not name.strip():
                st.error("Please enter your Full Name.")
            elif not phone.strip() or len(phone.strip()) < 10:
                st.error("Please enter a valid 10-digit Mobile Number.")
            elif not pass1 or len(pass1) < 4:
                st.error("Password must be at least 4 characters long.")
            elif pass1 != pass2:
                st.error("Passwords do not match. Please verify.")
            else:
                success, msg = auth.register(
                    name=name,
                    phone=phone,
                    email=email,
                    password=pass1,
                    state="" if state == "— Select —" else state,
                    category="" if category == "— Select —" else category,
                )
                if success:
                    st.toast(msg)
                    session.navigate("form_selection")
                else:
                    st.error(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div style="text-align:center;font-size:0.9rem;">'
            f'{t("reg_has_acct")}'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.button(t("reg_login_link"), use_container_width=True):
            session.navigate("login")

    spacer()
    info_box("🔒 Security Notice: Your personal details are encrypted and used solely for authenticating government scholarship applications.")
