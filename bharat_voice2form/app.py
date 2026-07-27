"""
app.py — Formitra (भारत Formitra)
==================================
Main Streamlit entry point.
"""

import streamlit as st

# ── 1. Page config — must be first ────────────────────────────────
st.set_page_config(
    page_title            = "Formitra — AI Voice Form Filling",
    page_icon             = "🎙️",
    layout                = "wide",
    initial_sidebar_state = "expanded",
)

# ── 2. Session state initialization ───────────────────────────────
import utils.session as session
session.init()

# ── 3. Dynamic Global CSS & Themes ─────────────────────────────────
from styles import inject_global_css
inject_global_css()

# ── 4. Sidebar navigation & branding ──────────────────────────────
from components.navbar import render_sidebar
render_sidebar()

# ── 5. Floating AI Assistant Widget ───────────────────────────────
from components.ai_assistant import render_ai_assistant_widget
render_ai_assistant_widget()

# ── 6. Page routing ────────────────────────────────────────────────
import views.home           as _home
import views.login          as _login
import views.register       as _register
import views.form_selection as _form_sel
import views.voice_input    as _voice
import views.ai_processing  as _ai
import views.auto_fill      as _fill
import views.preview        as _preview
import views.success        as _success
import views.track_status   as _track
import views.help_faq       as _help

_ROUTES: dict = {
    "home":           _home,
    "login":          _login,
    "register":       _register,
    "form_selection": _form_sel,
    "voice_input":    _voice,
    "ai_processing":  _ai,
    "auto_fill":      _fill,
    "preview":        _preview,
    "success":        _success,
    "track_status":   _track,
    "help_faq":       _help,
}

page_key = session.get("page", "home")
module   = _ROUTES.get(page_key)

if module is not None:
    module.render()
else:
    st.error(
        f"Unknown page: `{page_key}`. "
        f"Expected one of: {list(_ROUTES.keys())}"
    )
