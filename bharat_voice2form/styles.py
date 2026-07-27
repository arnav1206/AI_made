"""
styles.py
=========
Global design system & CSS injection for Formitra (भारत Formitra).
Comprehensive Light/Dark theme styling covering inputs, text, placeholders, popovers, audio input, tabs, cards, selectboxes, top header transparency, toolbar icons, and buttons.
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

        /* ── Streamlit Top Header Bar & Toolbar Icons Fix ── */
        header[data-testid="stHeader"], [data-testid="stHeader"] {{
            background-color: transparent !important;
            background: transparent !important;
        }}
        header[data-testid="stHeader"] button,
        header[data-testid="stHeader"] svg,
        header[data-testid="stHeader"] a,
        header[data-testid="stHeader"] span,
        header[data-testid="stHeader"] p {{
            color: {text_primary} !important;
            fill: {text_primary} !important;
            stroke: {text_primary} !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}
        header[data-testid="stHeader"] button:hover {{
            background-color: rgba(255, 122, 0, 0.15) !important;
            border-radius: 8px !important;
        }}

        /* ── Main Canvas Typography & Text ── */
        .stApp p, .stApp label,
        .stMarkdown p, .stMarkdown label,
        h1, h2, h3, h4, h5, h6 {{
            color: {text_primary} !important;
        }}

        /* ── Sidebar Container & Typography ── */
        section[data-testid="stSidebar"] {{
            background-color: {bg_sidebar} !important;
            color: #FFFFFF !important;
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
        }}
        section[data-testid="stSidebar"] .stMarkdown p,
        section[data-testid="stSidebar"] label {{
            color: #F8FAFC !important;
        }}

        /* ── Sidebar Navigation Buttons ── */
        section[data-testid="stSidebar"] .stButton > button {{
            background-color: rgba(255, 255, 255, 0.08) !important;
            color: #F8FAFC !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 50px !important;
            font-weight: 700 !important;
            font-size: 0.9rem !important;
            margin-bottom: 0.35rem !important;
            transition: all 0.2s ease !important;
            box-shadow: none !important;
        }}
        section[data-testid="stSidebar"] .stButton > button p,
        section[data-testid="stSidebar"] .stButton > button span,
        section[data-testid="stSidebar"] .stButton > button div {{
            color: #F8FAFC !important;
            font-weight: 700 !important;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover {{
            background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%) !important;
            color: #FFFFFF !important;
            border-color: transparent !important;
            box-shadow: 0 4px 15px rgba(255, 122, 0, 0.4) !important;
            transform: translateY(-1px) !important;
        }}
        section[data-testid="stSidebar"] .stButton > button:hover p,
        section[data-testid="stSidebar"] .stButton > button:hover span {{
            color: #FFFFFF !important;
        }}

        /* ── Universal High-Contrast Main Area Buttons Fix ── */
        .stMainBlockContainer .stButton > button,
        button[data-testid="stBaseButton-secondary"],
        button[data-testid="stBaseButton-primary"] {{
            border-radius: 50px !important;
            font-weight: 800 !important;
            padding: 0.65rem 1.5rem !important;
            transition: all 0.2s ease !important;
        }}

        /* Secondary Buttons (e.g. Load Sample Transcript, Clear, Edit) */
        .stMainBlockContainer .stButton > button:not([kind="primary"]),
        button[data-testid="stBaseButton-secondary"] {{
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border: 1.5px solid rgba(255, 122, 0, 0.45) !important;
        }}
        .stMainBlockContainer .stButton > button:not([kind="primary"]) p,
        .stMainBlockContainer .stButton > button:not([kind="primary"]) span,
        .stMainBlockContainer .stButton > button:not([kind="primary"]) div,
        button[data-testid="stBaseButton-secondary"] p,
        button[data-testid="stBaseButton-secondary"] span,
        button[data-testid="stBaseButton-secondary"] div {{
            color: #F8FAFC !important;
            -webkit-text-fill-color: #F8FAFC !important;
            font-weight: 800 !important;
        }}
        .stMainBlockContainer .stButton > button:not([kind="primary"]):hover,
        button[data-testid="stBaseButton-secondary"]:hover {{
            border-color: transparent !important;
            color: #FFFFFF !important;
            background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%) !important;
            box-shadow: 0 4px 15px rgba(255, 122, 0, 0.4) !important;
        }}
        .stMainBlockContainer .stButton > button:not([kind="primary"]):hover p,
        .stMainBlockContainer .stButton > button:not([kind="primary"]):hover span,
        button[data-testid="stBaseButton-secondary"]:hover p,
        button[data-testid="stBaseButton-secondary"]:hover span {{
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
        }}

        /* Primary Action Buttons */
        .stMainBlockContainer .stButton > button[kind="primary"],
        button[data-testid="stBaseButton-primary"],
        .stMainBlockContainer .stButton > button[kind="primary"] p,
        .stMainBlockContainer .stButton > button[kind="primary"] span,
        .stMainBlockContainer .stButton > button[kind="primary"] div,
        button[data-testid="stBaseButton-primary"] p,
        button[data-testid="stBaseButton-primary"] span,
        button[data-testid="stBaseButton-primary"] div {{
            background: linear-gradient(135deg, #FF7A00 0%, #EA580C 100%) !important;
            color: #FFFFFF !important;
            -webkit-text-fill-color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 4px 15px rgba(255, 122, 0, 0.4) !important;
            font-weight: 800 !important;
        }}

        /* ── Streamlit Audio Input Widget Fix ── */
        div[data-testid="stAudioInput"],
        [data-testid="stAudioInput"] > div,
        section[data-testid="stAudioInput"] {{
            background-color: {input_bg} !important;
            background: {input_bg} !important;
            border: 1.5px solid rgba(255, 122, 0, 0.45) !important;
            border-radius: 16px !important;
            color: {text_primary} !important;
        }}
        div[data-testid="stAudioInput"] button,
        div[data-testid="stAudioInput"] span,
        div[data-testid="stAudioInput"] div,
        div[data-testid="stAudioInput"] svg,
        div[data-testid="stAudioInput"] p {{
            color: {text_primary} !important;
            fill: {text_primary} !important;
            stroke: {text_primary} !important;
        }}
        div[data-testid="stAudioInput"] button:hover {{
            background-color: rgba(255, 122, 0, 0.2) !important;
        }}

        /* ── Voice Dictate Popover Buttons Fix ── */
        div[data-testid="stPopover"] > button,
        .stPopover > button {{
            background-color: {input_bg} !important;
            color: {text_primary} !important;
            border: 1px solid {border_col} !important;
            border-radius: 8px !important;
        }}
        div[data-testid="stPopover"] > button p,
        div[data-testid="stPopover"] > button span,
        div[data-testid="stPopover"] > button div,
        .stPopover > button p,
        .stPopover > button span {{
            color: {text_primary} !important;
            font-weight: 700 !important;
        }}
        div[data-testid="stPopover"] > button:hover {{
            border-color: #FF7A00 !important;
            background-color: rgba(255, 122, 0, 0.15) !important;
        }}
        div[data-testid="stPopover"] > button:hover p,
        div[data-testid="stPopover"] > button:hover span {{
            color: #FF7A00 !important;
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

        /* ── Input Fields & Text Area Placeholders Fix ── */
        .stTextInput input, .stTextArea textarea, .stNumberInput input {{
            background-color: {input_bg} !important;
            color: {input_text} !important;
            border: 1.5px solid {border_col} !important;
            border-radius: 12px !important;
            font-size: 0.95rem !important;
            padding: 0.6rem 0.9rem !important;
        }}
        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder,
        .stNumberInput input::placeholder {{
            color: #94A3B8 !important;
            opacity: 0.85 !important;
            -webkit-text-fill-color: #94A3B8 !important;
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
        .stExpander summary, .stExpander summary p, .stExpander summary span, .stExpander summary svg {{
            color: {text_primary} !important;
            font-weight: 700 !important;
            fill: {text_primary} !important;
        }}
    </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)
