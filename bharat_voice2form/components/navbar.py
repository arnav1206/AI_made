"""
components/navbar.py
====================
Sidebar navigation component with language selector, user auth status, Admin Portal link & Dark Mode toggle.
Features official Formitra darkmode multilingual brand logo positioned to the left & up.
"""

from __future__ import annotations

import base64
import streamlit as st

from utils.constants    import PAGE_ORDER, PAGE_LABELS
from utils.translations import t, get_available_languages
from components.layout  import tricolour_divider_inline
import utils.session as session
import utils.auth as auth


_NAV_KEYS: dict[str, str] = {
    "login":          "nav_login",
    "register":       "nav_register",
    "admin":          "nav_admin",
    "home":           "nav_home",
    "form_selection": "nav_form_selection",
    "voice_input":    "nav_voice_input",
    "ai_processing":  "nav_ai_processing",
    "auto_fill":      "nav_auto_fill",
    "preview":        "nav_preview",
    "success":        "nav_success",
    "track_status":   "nav_track_status",
    "help_faq":       "nav_help_faq",
}


def render_sidebar() -> None:
    """Render left sidebar: logo, user badge, theme toggle, language picker, nav."""
    with st.sidebar:
        _logo_block()
        _user_auth_badge()
        _theme_toggle_button()
        st.markdown(tricolour_divider_inline(4), unsafe_allow_html=True)
        _language_selector()
        st.markdown(tricolour_divider_inline(2), unsafe_allow_html=True)
        _nav_section()
        _context_badges()
        _footer_block()


def _logo_block() -> None:
    img_path = "bharat_voice2form/assets/images/multilingual_dark.jpg"

    try:
        with open(img_path, "rb") as f:
            b64_img = base64.b64encode(f.read()).decode("utf-8")
        logo_html = (
            f'<img src="data:image/jpeg;base64,{b64_img}" '
            f'style="width:90px;height:90px;border-radius:50%;object-fit:cover;'
            f'box-shadow:0 4px 18px rgba(255,122,0,0.4);border:2.5px solid #FF7A00;'
            f'display:block;margin:-10px auto 0.4rem auto;transform:translateX(-8px);" />'
        )
    except Exception:
        logo_html = '<div style="font-size:2.4rem;text-align:center;">🎙️</div>'

    st.markdown(
        f'<div style="text-align:center;padding:0.25rem 0 0.25rem;">'
        f'{logo_html}'
        f'<div style="font-size:1.35rem;font-weight:900;letter-spacing:-0.4px;color:#FF7A00;">'
        f'Formitra</div>'
        f'<div style="font-size:0.75rem;opacity:0.85;margin-top:0.1rem;color:#F8FAFC;">'
        f'AI Voice-Powered Form Filling</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _user_auth_badge() -> None:
    """Displays logged-in user profile or quick login link."""
    if auth.is_admin_logged_in():
        admin_user = st.session_state.get("admin_user", "Admin")
        st.markdown(
            f'<div style="background:rgba(37, 99, 235, 0.25);border:1px solid rgba(37, 99, 235, 0.6);'
            f'border-radius:10px;padding:0.5rem 0.75rem;text-align:center;margin-bottom:0.5rem;color:#F8FAFC;">'
            f'<div style="font-size:0.75rem;opacity:0.8;">ADMINISTRATOR LOGGED IN</div>'
            f'<div style="font-size:0.9rem;font-weight:800;color:#60A5FA;">🛡️ {admin_user.title()}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    elif auth.is_logged_in():
        user = auth.get_logged_in_user()
        name = user.get("name", "Applicant") if user else "Applicant"
        st.markdown(
            f'<div style="background:rgba(5, 150, 105, 0.2);border:1px solid rgba(5, 150, 105, 0.5);'
            f'border-radius:10px;padding:0.5rem 0.75rem;text-align:center;margin-bottom:0.5rem;color:#F8FAFC;">'
            f'<div style="font-size:0.75rem;opacity:0.8;">LOGGED IN ACCOUNT</div>'
            f'<div style="font-size:0.9rem;font-weight:800;color:#10B981;">👤 {name}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔑 Login", key="sb_login_btn", use_container_width=True):
                session.navigate("login")
        with c2:
            if st.button("📝 Register", key="sb_reg_btn", use_container_width=True):
                session.navigate("register")


def _theme_toggle_button() -> None:
    """Dark / Light mode switcher."""
    is_dark = session.get("dark_mode", False)
    btn_label = "☀️ Light Mode" if is_dark else "🌙 Dark Mode"
    if st.button(btn_label, key="theme_toggle_btn", use_container_width=True):
        session.set("dark_mode", not is_dark)
        st.rerun()


def _language_selector() -> None:
    """Language selectbox — visible text before & inside dropdown."""
    langs   = get_available_languages()
    current = session.get("selected_language", "Hindi")
    try:
        idx = langs.index(current)
    except ValueError:
        idx = 0

    st.markdown(
        f'<div style="font-size:0.88rem;font-weight:800;color:#F8FAFC;margin-bottom:0.3rem;">'
        f'{t("ui_language")}</div>',
        unsafe_allow_html=True,
    )
    chosen = st.selectbox(
        t("ui_language"),
        langs,
        index=idx,
        key="sidebar_lang_select",
        label_visibility="collapsed",
    )
    if chosen != current:
        session.set("selected_language", chosen)
        st.rerun()


def _nav_section() -> None:
    current_page = session.get("page", "home")

    st.markdown(
        f'<div style="font-size:0.72rem;font-weight:700;opacity:0.7;'
        f'text-transform:uppercase;letter-spacing:0.1em;margin-bottom:0.4rem;color:#F8FAFC;">'
        f'{t("nav_heading")}</div>',
        unsafe_allow_html=True,
    )

    for page_key in PAGE_ORDER:
        label = t(_NAV_KEYS.get(page_key, f"nav_{page_key}"))
        is_active = (page_key == current_page)

        btn_type  = "primary" if is_active else "secondary"
        btn_label = f"🔥 {label}" if is_active else label

        if st.button(
            btn_label,
            key=f"nav_{page_key}",
            use_container_width=True,
            type=btn_type,
        ):
            session.navigate(page_key)


def _context_badges() -> None:
    if sf := session.get("selected_form"):
        st.markdown(
            f'<div style="font-size:0.72rem;font-weight:700;opacity:0.7;'
            f'text-transform:uppercase;letter-spacing:0.1em;'
            f'margin-top:1.2rem;margin-bottom:0.3rem;color:#F8FAFC;">{t("selected_form_lbl")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="background:rgba(255,122,0,0.25);'
            f'border:1px solid rgba(255,122,0,0.5);border-radius:8px;'
            f'padding:0.45rem 0.75rem;font-size:0.82rem;font-weight:600;color:#F8FAFC;">'
            f'🎓 {sf}</div>',
            unsafe_allow_html=True,
        )

    if lang := session.get("selected_language"):
        st.markdown(
            f'<div style="font-size:0.72rem;font-weight:700;opacity:0.7;'
            f'text-transform:uppercase;letter-spacing:0.1em;'
            f'margin-top:0.6rem;margin-bottom:0.3rem;color:#F8FAFC;">{t("language_lbl")}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div style="background:rgba(19,136,8,0.25);'
            f'border:1px solid rgba(19,136,8,0.5);border-radius:8px;'
            f'padding:0.45rem 0.75rem;font-size:0.82rem;font-weight:600;color:#F8FAFC;">'
            f'🌐 {lang}</div>',
            unsafe_allow_html=True,
        )


def _footer_block() -> None:
    from utils.constants import APP_VERSION
    st.markdown(
        f'<div style="margin-top:2rem;padding:0.65rem;background:rgba(255,255,255,0.06);'
        f'border-radius:10px;text-align:center;border:1px solid rgba(255,255,255,0.1);">'
        f'<div style="font-size:0.75rem;opacity:0.9;font-weight:700;color:#F8FAFC;">'
        f'Formitra v{APP_VERSION}</div>'
        f'<div style="font-size:0.7rem;opacity:0.7;margin-top:0.1rem;color:#CBD5E1;">'
        f'{t("powered_by")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
