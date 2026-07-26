"""
styles.py
=========
Global design system & CSS injection for Formitra (भारत Formitra).
Includes Light/Dark theme switching, high-contrast selectbox text, horizontal step bar, and animated AI avatar styles.
"""

from __future__ import annotations
import streamlit as st


def inject_global_css() -> None:
    """Inject global CSS rules for Light/Dark mode and high-contrast UI components."""
    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        bg_main      = "#0B0F19"
        bg_card      = "#151C2C"
        bg_sidebar   = "#0F172A"
        text_primary = "#F8FAFC"
        text_sub     = "#94A3B8"
        border_col   = "rgba(255, 255, 255, 0.12)"
        select_bg    = "#1E293B"
        select_text  = "#FFFFFF"
    else:
        bg_main      = "#F8FAFC"
        bg_card      = "#FFFFFF"
        bg_sidebar   = "#0F172A"
        text_primary = "#0F172A"
        text_sub     = "#475569"
        border_col   = "#E2E8F0"
        select_bg    = "#FFFFFF"
        select_text  = "#0F172A"

    css_code = f"""
    <style>
        /* ── Core Layout & Background ── */
        .stApp {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            color: #FFFFFF !important;
            border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label {{
            color: #F8FAFC !important;
        }}

        /* ── Step Progress Bar Layout ── */
        .step-bar {{
            display: flex !important;
            flex-direction: row !important;
            align-items: center !important;
            justify-content: space-between !important;
            margin: 1rem 0 2rem 0 !important;
            width: 100% !important;
            padding: 0 0.5rem !important;
        }}
        .step-item {{
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            flex: 1 !important;
            position: relative !important;
        }}
        .step-circle {{
            width: 36px !important;
            height: 36px !important;
            border-radius: 50% !important;
            background: rgba(148, 163, 184, 0.2) !important;
            color: {text_sub} !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: 800 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.35rem !important;
            border: 2px solid transparent !important;
            transition: all 0.25s ease !important;
        }}
        .step-circle.active {{
            background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 15px rgba(255, 122, 0, 0.5) !important;
        }}
        .step-circle.done {{
            background: #059669 !important;
            color: #FFFFFF !important;
        }}
        .step-label {{
            font-size: 0.78rem !important;
            font-weight: 700 !important;
            text-align: center !important;
            color: {text_primary} !important;
        }}

        /* ── FIX: Language & Selectbox Dropdown Visibility ── */
        div[data-baseweb="select"] > div {{
            background-color: {select_bg} !important;
            color: {select_text} !important;
            border: 2px solid #FF7A00 !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
        }}
        div[data-baseweb="select"] span {{
            color: {select_text} !important;
            font-weight: 700 !important;
        }}
        ul[data-baseweb="menu"] {{
            background-color: {select_bg} !important;
            color: {select_text} !important;
        }}
        ul[data-baseweb="menu"] li {{
            color: {select_text} !important;
            font-weight: 600 !important;
        }}

        /* ── Cards & Containers ── */
        .card {{
            background-color: {bg_card} !important;
            color: {text_primary} !important;
            border-radius: 18px !important;
            padding: 1.5rem !important;
            border: 1px solid {border_col} !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.03) !important;
            margin-bottom: 1.25rem !important;
            transition: all 0.25s ease !important;
        }}
        .card:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.08) !important;
        }}

        /* ── Buttons ── */
        .stButton > button {{
            border-radius: 50px !important;
            font-weight: 700 !important;
            padding: 0.65rem 1.5rem !important;
            transition: all 0.2s ease !important;
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(255, 122, 0, 0.4) !important;
        }}
        .stButton > button[kind="primary"]:hover {{
            transform: translateY(-2px) scale(1.02) !important;
            box-shadow: 0 8px 22px rgba(255, 122, 0, 0.5) !important;
        }}

        /* ── Form Inputs ── */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {{
            background-color: {bg_card} !important;
            color: {text_primary} !important;
            border: 1.5px solid {border_col} !important;
            border-radius: 12px !important;
        }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
