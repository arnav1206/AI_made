"""
views/preview.py
================
Application preview page — translated via t().
100% Multilingual translation support.
Includes live, large-format high-fidelity PDF document receipt card & download option.
Uses components.html for 100% clean, unblocked native rendering across all browsers.
"""

import base64
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from components.layout   import tricolour_bar, section_heading, spacer
from components.progress import step_progress_bar
from components.cards    import preview_table, field_mapping_row
from utils.constants     import SCHOLARSHIP_SECTIONS
from utils.translations  import t
from utils.pdf_generator import generate as generate_pdf
import utils.session as session


def _get_logo_b64() -> str:
    img_path = Path(__file__).parent.parent / "assets" / "images" / "logo.png"
    if img_path.exists():
        try:
            return base64.b64encode(img_path.read_bytes()).decode("utf-8")
        except Exception:
            return ""
    return ""


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
        f'<div style="margin-top:0.4rem;background:rgba(16,185,129,0.2);border:1px solid #10B981;padding:0.25rem 0.55rem;border-radius:6px;font-size:0.72rem;font-weight:800;color:#34D399;display:inline-block;">📱 Digital QR Verification Enabled</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    section_key_map = {
        "Personal Information":       t("section_personal"),
        "Address & Domicile Details": t("section_address"),
        "Academic Information":       t("section_academic"),
        "Financial & Contact Details": t("section_financial"),
    }

    dynamic_qs     = session.get("dynamic_form_questions")
    extracted_data = session.get("extracted_data", {})
    is_google_form = bool(dynamic_qs) or session.get("is_google_form_imported") or ("Google Form" in str(form_name))

    # ── Section tables ─────────────────────────────────────────────
    if is_google_form:
        q_items = dynamic_qs if dynamic_qs else [{"id": f"eq_{i}", "title": k} for k in extracted_data.keys()]
        st.markdown(
            f'<div class="card" style="border-left:5px solid #FF7A00;margin-bottom:1.5rem;">'
            f'<div style="font-weight:800;font-size:1.1rem;color:#FF7A00;margin-bottom:0.5rem;">'
            f'📋 Imported Google Form Questions ({len(q_items)} Questions)</div>'
            f'<div style="font-size:0.88rem;opacity:0.85;margin-bottom:1rem;">'
            f'Extracted values from voice input for your imported Google Form:</div>',
            unsafe_allow_html=True,
        )

        for q in q_items:
            q_title = q["title"]
            val = form_data.get(q_title) or extracted_data.get(q_title) or "—"
            if val == "—":
                for k, v in extracted_data.items():
                    if v and (k.lower() in q_title.lower() or q_title.lower() in k.lower()):
                        val = v
                        break
            field_mapping_row(label=q_title, value=str(val), found=(val != "—"))

        st.markdown('</div>', unsafe_allow_html=True)
    else:
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

    # ── Pre-Generate PDF Document for Download ──────────────
    pdf_res = generate_pdf(
        form_data=extracted_data if is_google_form else form_data,
        application_no=app_no,
        form_title=form_name,
    )

    # ── High-Fidelity Official PDF Receipt Document Card ──
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📄 Official PDF Application Receipt Preview (Full Document View)", expanded=True):
        logo_b64 = _get_logo_b64()
        logo_tag = f'<img src="data:image/png;base64,{logo_b64}" width="48" height="48" style="border-radius:8px;object-fit:contain;background:#0F172A;padding:2px;" />' if logo_b64 else '<span style="font-size:2rem;">🏛️</span>'

        if is_google_form:
            items = []
            q_items = dynamic_qs if dynamic_qs else [{"title": k} for k in extracted_data.keys()]
            for q in q_items:
                q_t = q["title"]
                v = form_data.get(q_t) or extracted_data.get(q_t) or "—"
                if v == "—":
                    for k, val_found in extracted_data.items():
                        if val_found and (k.lower() in q_t.lower() or q_t.lower() in k.lower()):
                            v = val_found
                            break
                items.append((q_t, str(v)))
            if not items:
                items = list(extracted_data.items())

            for q in q_items:
                q_t = q["title"]
                v = form_data.get(q_t) or extracted_data.get(q_t) or "—"
                if v == "—":
                    for k, val_found in extracted_data.items():
                        if val_found and (k.lower() in q_t.lower() or q_t.lower() in k.lower()):
                            v = val_found
                            break
                items.append((q_t, str(v)))
            if not items:
                items = list(extracted_data.items())
        else:
            items = list(form_data.items()) if form_data else list(extracted_data.items())

        grid_rows = ""
        for idx, (k, v) in enumerate(items):
            bg = "#F8FAFC" if idx % 2 == 0 else "#FFFFFF"
            grid_rows += (
                f'<div style="display:flex;justify-content:space-between;padding:0.65rem 1rem;background:{bg};border-bottom:1px solid #E2E8F0;">'
                f'<span style="font-weight:700;color:#0F172A;font-size:0.9rem;">{k}</span>'
                f'<span style="font-weight:500;color:#334155;font-size:0.9rem;">{v or "—"}</span>'
                f'</div>'
            )

        card_html = (
            f'<!DOCTYPE html><html><head><meta charset="utf-8"/></head><body style="margin:0;padding:10px;background:transparent;">'
            f'<div style="background:#FFFFFF;color:#0F172A;border-radius:16px;padding:1.5rem;border:3px solid #FF7A00;box-shadow:0 12px 35px rgba(255, 122, 0, 0.35);font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif;">'
            f'<div style="background:#0B132B;color:#FFFFFF;padding:1.25rem 1.5rem;border-radius:12px;display:flex;justify-content:space-between;align-items:center;margin-bottom:0;">'
            f'<div style="display:flex;align-items:center;gap:1rem;">'
            f'{logo_tag}'
            f'<div>'
            f'<div style="font-weight:900;font-size:1.1rem;color:#FFFFFF;letter-spacing:-0.3px;">NATIONAL SCHOLARSHIP PORTAL — GOVT OF INDIA</div>'
            f'<div style="font-size:0.82rem;color:#CBD5E1;margin-top:0.2rem;">Formitra AI Voice-Assisted Official Application Receipt</div>'
            f'</div>'
            f'</div>'
            f'<div style="text-align:right;">'
            f'<div style="font-size:0.75rem;color:#94A3B8;font-weight:700;">APPLICATION REF NO</div>'
            f'<div style="font-size:1.15rem;font-weight:900;color:#FDE047;font-family:monospace;">{app_no}</div>'
            f'<div style="font-size:0.75rem;color:#CBD5E1;margin-top:0.1rem;">Date: {now}</div>'
            f'</div>'
            f'</div>'
            f'<div style="display:flex;height:4px;margin-bottom:1.25rem;">'
            f'<div style="flex:1;background:#FF7A00;"></div>'
            f'<div style="flex:1;background:#FFFFFF;"></div>'
            f'<div style="flex:1;background:#059669;"></div>'
            f'</div>'
            f'<div style="font-size:1.1rem;font-weight:800;color:#0F172A;margin-bottom:0.4rem;">📋 Application Details: {form_name}</div>'
            f'<hr style="border:none;border-top:2px solid #FF7A00;margin-bottom:1.25rem;" />'
            f'<div style="border:1px solid #CBD5E1;border-radius:10px;overflow:hidden;margin-bottom:1.25rem;box-shadow:0 2px 8px rgba(0,0,0,0.04);">{grid_rows}</div>'
            f'<div style="background:#FEF3C7;border:1.5px solid #F59E0B;padding:0.9rem 1.25rem;border-radius:10px;margin-bottom:1.25rem;">'
            f'<div style="font-weight:800;font-size:0.92rem;color:#92400E;margin-bottom:0.25rem;">📜 Applicant Self-Declaration & Authenticity Verification</div>'
            f'<div style="font-size:0.85rem;color:#78350F;line-height:1.5;">I hereby declare that all information provided above is true and correct to the best of my knowledge. I understand that any false statement will disqualify my scholarship application under the National Scholarship Portal rules.</div>'
            f'</div>'
            f'<div style="text-align:center;padding:0.75rem;background:#F1F5F9;border-radius:8px;font-size:0.85rem;color:#334155;font-weight:700;border:1px dashed #94A3B8;">✅ Official Formitra Digital Application Receipt | Ref: <b>{app_no}</b> | Verified & Sealed Electronically</div>'
            f'</div></body></html>'
        )
        components.html(card_html, height=720, scrolling=True)

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
