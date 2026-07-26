"""
views/form_selection.py
=======================
Form type selection grid page — distinct boxed options for scholarship schemes.
"""

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

    cols = st.columns(3, gap="medium")

    for i, form in enumerate(FORM_TYPES):
        col_idx = i % 3
        if col_idx == 0 and i != 0:
            spacer(0.5)
            cols = st.columns(3, gap="medium")

        with cols[col_idx]:
            # Enclose each scheme option in its own distinct card box
            border_accent = "#FF7A00" if i == 0 else "#2563EB" if i == 1 else "#059669" if i == 2 else "#9333EA" if i == 3 else "#94A3B8"
            
            st.markdown(
                f'<div class="card" style="border-top: 5px solid {border_accent}; min-height: 220px; display: flex; flex-direction: column; justify-content: space-between;">'
                f'<div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.6rem;">'
                f'<span style="font-size:2.2rem;">{form["icon"]}</span>'
                f'<span style="background:{"rgba(5, 150, 105, 0.15)" if form["available"] else "rgba(148, 163, 184, 0.15)"};color:{"#059669" if form["available"] else "#64748B"};padding:0.25rem 0.65rem;border-radius:20px;font-size:0.75rem;font-weight:800;">{form["badge"]}</span>'
                f'</div>'
                f'<div style="font-weight:800;font-size:1.08rem;margin-bottom:0.4rem;line-height:1.3;">{form["title"]}</div>'
                f'<div style="font-size:0.85rem;opacity:0.82;line-height:1.5;margin-bottom:1rem;">{form["desc"]}</div>'
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
                    session.set("selected_form", form["title"])
                    session.navigate("voice_input")
            else:
                st.button(
                    t("coming_soon"),
                    key=f"form_{i}",
                    use_container_width=True,
                    disabled=True,
                )

    spacer()
    info_box(t("prototype_info"))
