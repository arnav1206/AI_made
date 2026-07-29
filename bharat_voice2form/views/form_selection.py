"""
views/form_selection.py
=======================
Form type selection grid page — distinct boxed options for scholarship schemes
with Google Forms & Custom Form Link Importer and automatic Voice Input navigation.
100% Multilingual translation support via t().
"""

import time
import streamlit as st

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.constants     import FORM_TYPES
from utils.translations  import t
import utils.session as session


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=1)

    section_heading(t("select_form"), t("select_form_sub"))

    is_dark = st.session_state.get("dark_mode", False)
    card_bg = "#1E293B" if is_dark else "#F8FAFC"
    border_col = "rgba(255, 122, 0, 0.4)" if is_dark else "#FED7AA"

    # ── 1. Custom Google Forms & Web Form URL Importer ─────────────
    st.markdown(
        f'<div class="card" style="border-left:5px solid #FF7A00;background:{card_bg};border:1px solid {border_col};margin-bottom:2rem;">'
        f'<div style="font-weight:800;font-size:1.1rem;color:#FF7A00;margin-bottom:0.3rem;">'
        f'{t("import_form_title")}</div>'
        f'<div style="font-size:0.88rem;opacity:0.85;margin-bottom:0.85rem;line-height:1.5;">'
        f'{t("import_form_sub")}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    c_url1, c_url2 = st.columns([3, 1])
    with c_url1:
        custom_url = st.text_input(
            "Paste Form URL (Google Forms / NSP Portal)",
            placeholder="e.g. https://docs.google.com/forms/d/e/1FAIpQLSc...",
            key="custom_form_url_input",
            label_visibility="collapsed",
        )
    with c_url2:
        if st.button(t("analyze_fill_btn"), use_container_width=True, type="primary"):
            if custom_url.strip():
                url_str = custom_url.strip()
                form_title = "Google Forms Application" if "google.com" in url_str else "External Web Form"
                
                # Popup 1: Importing status notification
                st.toast("⏳ Importing & Analyzing Form Questions... Please wait.", icon="⏳")
                time.sleep(0.5)

                session.set("selected_form", f"{form_title} ({url_str[:35]}...)")
                session.set("custom_form_url", url_str)
                
                # Popup 2: Success notification & navigate to voice input page
                st.toast("🎉 Form questions imported successfully! Taking you to Voice Input...", icon="🎉")
                time.sleep(0.3)

                session.navigate("voice_input")
                st.rerun()
            else:
                st.warning("Please paste a valid form URL or select a scheme below.")

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,122,0,0.2);margin:1.5rem 0;'>", unsafe_allow_html=True)
    st.markdown(f'### {t("select_schemes_header")}')

    # ── 2. Standard Scholarship Form Grid ──────────────────────────
    cols = st.columns(3, gap="medium")

    for i, form in enumerate(FORM_TYPES):
        col_idx = i % 3
        if col_idx == 0 and i != 0:
            spacer(0.5)
            cols = st.columns(3, gap="medium")

        with cols[col_idx]:
            border_accent = "#FF7A00" if i == 0 else "#2563EB" if i == 1 else "#059669" if i == 2 else "#9333EA" if i == 3 else "#94A3B8"
            scheme_title  = t(f"scheme_{i}_title", form["title"])
            scheme_desc   = t(f"scheme_{i}_desc", form["desc"])
            badge_text    = t("available_now", "Available Now") if form["available"] else t("coming_soon", "Coming Soon")
            
            st.markdown(
                f'<div class="card" style="border-top: 5px solid {border_accent}; min-height: 220px; display: flex; flex-direction: column; justify-content: space-between;">'
                f'<div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">'
                f'<span style="font-size:2.2rem;">{form["icon"]}</span>'
                f'<span style="background:{"rgba(5, 150, 105, 0.15)" if form["available"] else "rgba(148, 163, 184, 0.15)"};color:{"#059669" if form["available"] else "#64748B"};padding:0.25rem 0.65rem;border-radius:20px;font-size:0.75rem;font-weight:800;">{badge_text}</span>'
                f'</div>'
                f'<div style="font-weight:800;font-size:1.08rem;margin-bottom:0.4rem;line-height:1.3;">{scheme_title}</div>'
                f'<div style="font-size:0.85rem;opacity:0.82;line-height:1.5;margin-bottom:1rem;">{scheme_desc}</div>'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )
            
            if form["available"]:
                if st.button(
                    t("select_btn"),
                    key=f"form_{i}",
                    use_container_width=True,
                    type="primary",
                ):
                    session.set("selected_form", scheme_title)
                    session.navigate("voice_input")
                    st.rerun()
            else:
                st.button(
                    t("coming_soon"),
                    key=f"form_{i}",
                    use_container_width=True,
                    disabled=True,
                )

    spacer()
    info_box(t("prototype_info"))
