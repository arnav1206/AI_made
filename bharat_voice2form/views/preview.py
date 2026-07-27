"""
views/preview.py
================
Application preview page — translated via t().
Includes live PDF document preview & download.
"""

import base64
import time
from datetime import datetime

import streamlit as st

from components.layout   import tricolour_bar, section_heading, spacer
from components.progress import step_progress_bar
from components.cards    import preview_table
from utils.constants     import SCHOLARSHIP_SECTIONS
from utils.translations  import t
from utils.pdf_generator import generate as generate_pdf
import utils.session as session


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=5)

    section_heading(t("preview_title"), t("preview_sub"))

    form_data = session.get("form_data", {})
    app_no    = session.generate_application_number()
    now       = datetime.now().strftime("%d %b %Y, %I:%M %p")
    form_name = session.get("selected_form") or "Merit-cum-Means Scholarship 2025-26"

    is_dark = st.session_state.get("dark_mode", False)

    if is_dark:
        dec_bg     = "rgba(217, 119, 6, 0.2)"
        dec_border = "1px solid rgba(245, 158, 11, 0.5)"
        dec_title  = "#FBBF24"
        dec_txt    = "#F8FAFC"
        hint_col   = "#CBD5E1"
    else:
        dec_bg     = "linear-gradient(135deg,#FFFBEB,#FEF3C7)"
        dec_border = "1px solid #FDE68A"
        dec_title  = "#92400E"
        dec_txt    = "#374151"
        hint_col   = "#64748B"

    # ── Application header banner ──────────────────────────────────
    st.markdown(
        f'<div style="background:linear-gradient(135deg,#002868,#004AD4);color:white;'
        f'border-radius:16px;padding:1.5rem 2rem;margin-bottom:1.5rem;">'
        f'<div style="display:flex;justify-content:space-between;align-items:flex-start;">'
        f'<div>'
        f'<div style="font-size:0.75rem;opacity:0.7;text-transform:uppercase;'
        f'letter-spacing:0.1em;">National Scholarship Portal — Government of India</div>'
        f'<div style="font-size:1.4rem;font-weight:800;margin:0.3rem 0;color:#FFFFFF !important;">'
        f'{form_name}</div>'
        f'<div style="font-size:0.88rem;opacity:0.85;color:#E0F2FE;">Bharat Voice2Form — AI Assisted Application</div>'
        f'</div>'
        f'<div style="text-align:right;">'
        f'<div style="font-size:0.75rem;opacity:0.7;color:#E0F2FE;">{t("app_number")}</div>'
        f'<div style="font-size:1rem;font-weight:700;font-family:monospace;color:#FDE047;">{app_no}</div>'
        f'<div style="font-size:0.78rem;opacity:0.7;margin-top:0.2rem;color:#E0F2FE;">Generated: {now}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # ── Section tables ─────────────────────────────────────────────
    for section in SCHOLARSHIP_SECTIONS:
        preview_table(
            section_title=f'{section["icon"]} {section["title"]}',
            fields=section["fields"],
            form_data=form_data,
        )

    # ── Declaration ────────────────────────────────────────────────
    st.markdown(
        f'<div class="form-card" style="background:{dec_bg};border:{dec_border};">'
        f'<div style="font-weight:800;font-size:0.98rem;color:{dec_title};margin-bottom:0.5rem;">{t("declaration_title")}</div>'
        f'<div style="font-size:0.88rem;color:{dec_txt};line-height:1.7;">'
        f'{t("declaration_text")}'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    agreed = st.checkbox(t("declaration_check"), key="declaration_agreed")

    # ── Pre-Generate PDF Document for Live Preview ──────────────────
    pdf_res = generate_pdf(
        form_data=form_data,
        application_no=app_no,
        form_title=form_name,
    )

    # ── Live PDF Document Preview Box ──────────────────────────────
    if pdf_res:
        with st.expander("👁️ Live Preview Generated PDF Document Before Download", expanded=False):
            b64_pdf = base64.b64encode(pdf_res.pdf_bytes).decode("utf-8")
            st.markdown(
                f'<iframe src="data:application/pdf;base64,{b64_pdf}" width="100%" height="450" type="application/pdf" style="border:1.5px solid rgba(255,122,0,0.4);border-radius:12px;box-shadow:0 4px 20px rgba(0,0,0,0.2);"></iframe>',
                unsafe_allow_html=True,
            )

    # ── Action buttons ─────────────────────────────────────────────
    spacer()
    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button(t("btn_edit"), use_container_width=True):
            session.navigate("auto_fill")

    with b2:
        if pdf_res:
            st.download_button(
                label="📄 Download Form (PDF)",
                data=pdf_res.pdf_bytes,
                file_name=pdf_res.filename,
                mime="application/pdf",
                use_container_width=True,
            )

    with b3:
        if st.button(
            t("btn_submit"),
            use_container_width=True,
            type="primary",
            disabled=not agreed,
        ):
            session.navigate("success")

    if not agreed:
        st.markdown(
            f'<div style="text-align:center;font-size:0.85rem;color:{hint_col};margin-top:0.4rem;font-weight:500;">'
            f'{t("accept_declaration")}'
            f'</div>',
            unsafe_allow_html=True,
        )
