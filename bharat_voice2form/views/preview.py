"""
views/preview.py
================
Application preview page — translated via t().
100% Multilingual translation support.
Includes live, large-format PDF document preview & download option.
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

    is_dark = st.session_state.get("dark_mode", True)

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
        f'letter-spacing:0.1em;">{t("nsp_portal_hdr")}</div>'
        f'<div style="font-size:1.4rem;font-weight:800;margin:0.3rem 0;color:#FFFFFF !important;">'
        f'{form_name}</div>'
        f'<div style="font-size:0.88rem;opacity:0.85;color:#E0F2FE;">{t("ai_assisted_app_sub")}</div>'
        f'</div>'
        f'<div style="text-align:right;">'
        f'<div style="font-size:0.75rem;opacity:0.7;color:#E0F2FE;">{t("app_number")}</div>'
        f'<div style="font-size:1rem;font-weight:700;font-family:monospace;color:#FDE047;">{app_no}</div>'
        f'<div style="font-size:0.78rem;opacity:0.7;margin-top:0.2rem;color:#E0F2FE;">Generated: {now}</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    section_key_map = {
        "Personal Information":       t("section_personal"),
        "Address & Domicile Details": t("section_address"),
        "Academic Information":       t("section_academic"),
        "Financial & Contact Details": t("section_financial"),
    }

    # ── Section tables ─────────────────────────────────────────────
    for section in SCHOLARSHIP_SECTIONS:
        sec_title = section_key_map.get(section["title"], f'{section["icon"]} {section["title"]}')
        preview_table(
            section_title=sec_title,
            fields=section["fields"],
            form_data=form_data,
        )

    # ── Declaration ────────────────────────────────────────────────
    st.markdown(
        f'<div class="form-card" style="background:{dec_bg};border:{dec_border};margin-bottom:1.5rem;">'
        f'<div style="font-weight:800;font-size:0.98rem;color:{dec_title};margin-bottom:0.5rem;">{t("declaration_title")}</div>'
        f'<div style="font-size:0.88rem;color:{dec_txt};line-height:1.7;">'
        f'{t("declaration_text")}'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    agreed = st.checkbox(t("declaration_check"), key="declaration_agreed")

    # ── Pre-Generate PDF Document for Live Big Preview ──────────────
    pdf_res = generate_pdf(
        form_data=form_data,
        application_no=app_no,
        form_title=form_name,
    )

    # ── Large-Format Live PDF Document Preview ─────────────────────
    if pdf_res:
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("📄 Official PDF Application Receipt Preview (Full Document View)", expanded=True):
            b64_pdf = base64.b64encode(pdf_res.pdf_bytes).decode("utf-8")
            
            grid_items = "".join(
                f'<div style="display:flex;justify-content:space-between;padding:0.45rem 0.8rem;border-bottom:1px solid #E2E8F0;'
                f'background:{"#F8FAFC" if idx % 2 == 0 else "#FFFFFF"};">'
                f'<span style="font-weight:700;color:#0F172A;font-size:0.85rem;">{k}:</span>'
                f'<span style="color:#334155;font-size:0.85rem;">{v or "—"}</span></div>'
                for idx, (k, v) in enumerate(form_data.items())
            ) if form_data else ""

            doc_fallback = f"""
            <iframe src="data:application/pdf;base64,{b64_pdf}#toolbar=1&navpanes=0&scrollbar=1" width="100%" height="750px" style="border:3px solid #FF7A00;border-radius:16px;box-shadow:0 12px 40px rgba(255, 122, 0, 0.35);">
                <object data="data:application/pdf;base64,{b64_pdf}" type="application/pdf" width="100%" height="750px">
                    <div style="background:#FFFFFF;color:#0F172A;padding:1.5rem;border-radius:12px;border:2px solid #FF7A00;">
                        <div style="background:#0F172A;color:#FFFFFF;padding:1rem;border-radius:8px;margin-bottom:0.75rem;">
                            <div style="font-weight:800;font-size:1.1rem;color:#FF7A00;">{t("nsp_portal_hdr")}</div>
                            <div style="font-size:0.85rem;color:#E2E8F0;">Formitra AI Voice Application Receipt | Ref: {app_no}</div>
                        </div>
                        <div style="margin-bottom:1rem;">{grid_items}</div>
                        <div style="background:#FEF3C7;border:1px solid #F59E0B;padding:0.75rem;border-radius:6px;font-size:0.8rem;color:#92400E;">
                            <b>📜 {t("receipt_sealed")}</b>
                        </div>
                    </div>
                </object>
            </iframe>
            """
            st.markdown(doc_fallback, unsafe_allow_html=True)

    # ── Action buttons ─────────────────────────────────────────────
    spacer()
    b1, b2, b3 = st.columns(3)

    with b1:
        if st.button(t("btn_edit"), use_container_width=True):
            session.navigate("auto_fill")

    with b2:
        if pdf_res:
            st.download_button(
                label=t("btn_download_pdf"),
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
