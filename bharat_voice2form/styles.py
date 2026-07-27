"""
styles.py
=========
Global design system & CSS injection for Formitra (भारत Formitra).
Comprehensive Light/Dark theme styling covering inputs, text, tabs, cards, selectboxes, and navigation.
"""

from __future__ import annotations
import streamlit as st


def inject_global_css() -> None:
    """Inject global CSS rules for Light/Dark mode and high-contrast UI components."""
    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        bg_main      = "#0B0F17"
        bg_card      = "#151C2C"
        bg_sidebar   = "#0F172A"
        text_primary = "#F8FAFC"
        text_sub     = "#CBD5E1"
        border_col   = "rgba(255, 255, 255, 0.15)"
        input_bg     = "#1E293B"
        input_text   = "#F8FAFC"
        select_bg    = "#1E293B"
        select_text  = "#F8FAFC"
        card_shadow  = "0 10px 30px rgba(0, 0, 0, 0.5)"
    else:
        bg_main      = "#F8FAFC"
        bg_card      = "#FFFFFF"
        bg_sidebar   = "#0F172A"
        text_primary = "#0F172A"
        text_sub     = "#475569"
        border_col   = "#E2E8F0"
        input_bg     = "#FFFFFF"
        input_text   = "#0F172A"
        select_bg    = "#FFFFFF"
        select_text  = "#0F172A"
        card_shadow  = "0 10px 25px -5px rgba(0, 0, 0, 0.05)"

    css_code = f"""
    <style>
        /* ── Core Layout & Background ── */
        .stApp {{
            background-color: {bg_main} !important;
            color: {text_primary} !important;
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
        }}

        /* ── Global Typography & Text Overrides ── */
        .stApp p, .stApp span, .stApp label, .stApp div,
        .stMarkdown p, .stMarkdown span, .stMarkdown label,
        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
        }}

        /* ── Sidebar ── */
        section[data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            color: #FFFFFF !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {{
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
            width: 38px !important;
            height: 38px !important;
            border-radius: 50% !important;
            background: rgba(148, 163, 184, 0.25) !important;
            color: {text_sub} !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            font-weight: 800 !important;
            font-size: 0.95rem !important;
            margin-bottom: 0.4rem !important;
            border: 2px solid transparent !important;
            transition: all 0.25s ease !important;
        }}
        .step-circle.active {{
            background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%) !important;
            color: #FFFFFF !important;
            box-shadow: 0 0 18px rgba(255, 122, 0, 0.55) !important;
        }}
        .step-circle.done {{
            background: #059669 !important;
            color: #FFFFFF !important;
        }}
        .step-label {{
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            text-align: center !important;
            color: {text_primary} !important;
        }}

        /* ── Input Fields & Text Areas ── */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1.5px solid {border_col} !important;
            border-radius: 12px !important;
            font-size: 0.95rem !important;
            padding: 0.6rem 0.9rem !important;
        }}
        .stTextInput input:focus, .stTextArea textarea:focus {{
            border-color: #FF7A00 !important;
            box-shadow: 0 0 0 2px rgba(255, 122, 0, 0.25) !important;
        }}

        /* ── Selectboxes & Dropdowns ── */
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
            border: 1px solid {border_col} !important;
        }}
        ul[data-baseweb="menu"] li {{
            color: {select_text} !important;
            font-weight: 600 !important;
        }}
        ul[data-baseweb="menu"] li:hover {{
            background-color: rgba(255, 122, 0, 0.2) !important;
        }}

        /* ── Tabs Styling ── */
        button[data-baseweb="tab"] {{
            color: {text_sub} !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            border-radius: 8px !important;
        }}
        button[data-baseweb="tab"][aria-selected="true"] {{
            color: #FF7A00 !important;
            border-bottom-color: #FF7A00 !important;
        }}

        /* ── Cards & Containers ── */
        .card {{
            background-color: {bg_card} !important;
            color: {text_primary} !important;
            border-radius: 18px !important;
            padding: 1.5rem !important;
            border: 1px solid {border_col} !important;
            box-shadow: {card_shadow} !important;
            margin-bottom: 1.25rem !important;
            transition: all 0.25s ease !important;
        }}
        .card:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15) !important;
        }}

        /* ── Expanders & Accordions ── */
        .stExpander {{
            background-color: {bg_card} !important;
            border: 1px solid {border_col} !important;
            border-radius: 14px !important;
            color: {text_primary} !important;
        }}
        .stExpander summary {{
            color: {text_primary} !important;
            font-weight: 700 !important;
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
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
