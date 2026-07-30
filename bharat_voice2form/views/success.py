"""
views/success.py
=================
Submission success page for Formitra.
100% Multilingual translation support via t().
Features celebratory green badge animation, ref code display, high-fidelity document receipt card & download option.
Uses components.html for 100% clean, unblocked native rendering across all browsers.
"""

import base64
import random
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.translations  import t
from utils.voice_assist  import render_voice_assistant_player
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

    # Generate or retrieve unique reference tracking code
    if not session.get("reference_code"):
        code_num = random.randint(10000, 99999)
        ref_code = f"FMT-2026-{code_num}"
        session.set("reference_code", ref_code)
        session.set("active_ref_code", ref_code)
    else:
        ref_code = session.get("reference_code")

    form_title     = session.get("selected_form") or "Scholarship Application"
    language       = session.get("selected_language", "English")
    form_data      = session.get("form_data", {})
    now            = datetime.now().strftime("%d %b %Y, %I:%M %p")
    dynamic_qs     = session.get("dynamic_form_questions")
    extracted_data = session.get("extracted_data", {})
    is_google_form = bool(dynamic_qs) or session.get("is_google_form_imported") or ("Google Form" in str(form_title))

    # Generate PDF document for download
    pdf_res = generate_pdf(
        form_data=extracted_data if is_google_form else form_data,
        application_no=ref_code,
        form_title=form_title,
    )

    title_translated = t("success_title", "Application Submitted Successfully!")
    ref_lbl_translated = t("ref_code_lbl", "FORMITRA REFERENCE CODE:")

    # ── Celebration HTML/CSS Confetti & Pulse Animation ─────────────
    animation_html = f"""<style>
.celebration-container {{
background: linear-gradient(135deg, #065F46 0%, #047857 50%, #064E3B 100%);
border-radius: 24px;
padding: 3rem 2rem;
color: #FFFFFF !important;
text-align: center;
position: relative;
overflow: hidden;
box-shadow: 0 20px 50px rgba(6, 95, 70, 0.4);
border: 2px solid #34D399;
margin-bottom: 2rem;
}}
.badge-ripple {{
width: 100px;
height: 100px;
margin: 0 auto 1.25rem;
background: #10B981;
border-radius: 50%;
display: flex;
align-items: center;
justify-content: center;
font-size: 3.5rem;
box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7);
animation: ripple 1.8s infinite ease-out;
}}
@keyframes ripple {{
0% {{ box-shadow: 0 0 0 0 rgba(52, 211, 153, 0.7); transform: scale(0.95); }}
70% {{ box-shadow: 0 0 0 30px rgba(52, 211, 153, 0); transform: scale(1.05); }}
100% {{ box-shadow: 0 0 0 0 rgba(52, 211, 153, 0); transform: scale(0.95); }}
}}
.confetti-particle {{
position: absolute;
width: 10px;
height: 10px;
background: #FBBF24;
opacity: 0.8;
animation: fall 3s infinite ease-in-out;
}}
@keyframes fall {{
0% {{ transform: translateY(-20px) rotate(0deg); opacity: 1; }}
100% {{ transform: translateY(300px) rotate(360deg); opacity: 0; }}
}}
</style>
<div class="celebration-container">
<div class="confetti-particle" style="left:10%;animation-delay:0s;background:#FBBF24;"></div>
<div class="confetti-particle" style="left:25%;animation-delay:0.4s;background:#34D399;"></div>
<div class="confetti-particle" style="left:40%;animation-delay:0.8s;background:#F472B6;"></div>
<div class="confetti-particle" style="left:60%;animation-delay:0.2s;background:#60A5FA;"></div>
<div class="confetti-particle" style="left:75%;animation-delay:0.6s;background:#FBBF24;"></div>
<div class="confetti-particle" style="left:90%;animation-delay:1s;background:#A7F3D0;"></div>

<div class="badge-ripple">✅</div>
<div style="font-size:2.2rem;font-weight:900;letter-spacing:-0.5px;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;">
{title_translated}
</div>
<div style="font-size:1.05rem;color:#D1FAE5 !important;-webkit-text-fill-color:#D1FAE5 !important;margin-top:0.5rem;">
{t("success_sub")} <b>{form_title}</b>
</div>

<div style="margin-top:1.75rem;display:inline-block;background:rgba(255, 255, 255, 0.15);backdrop-filter:blur(8px);padding:1rem 2.2rem;border-radius:50px;border:2px dashed #A7F3D0;">
<span style="font-size:0.85rem;color:#E6F4EA !important;-webkit-text-fill-color:#E6F4EA !important;font-weight:700;">{ref_lbl_translated} </span>
<span style="font-size:1.5rem;font-weight:900;color:#FDE047 !important;-webkit-text-fill-color:#FDE047 !important;letter-spacing:1.5px;">{ref_code}</span>
</div>
</div>"""

    st.markdown(animation_html, unsafe_allow_html=True)

    # Voice Speech Announcement
    tts_text = f"Congratulations! Your application for {form_title} has been submitted successfully. Your reference code is {ref_code}."
    render_voice_assistant_player(text=tts_text, language=language, label=f"🔊 {t('success_listen')} ({language})")

    spacer()

    # Large-Format High-Fidelity PDF Document Preview Card
    if pdf_res:
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
                f'<div style="background:#FFFFFF;color:#0F172A;border-radius:16px;padding:1.5rem;border:3px solid #10B981;box-shadow:0 12px 35px rgba(16, 185, 129, 0.35);font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,sans-serif;">'
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
                f'<div style="font-size:1.15rem;font-weight:900;color:#FDE047;font-family:monospace;">{ref_code}</div>'
                f'<div style="font-size:0.75rem;color:#CBD5E1;margin-top:0.1rem;">Date: {now}</div>'
                f'</div>'
                f'</div>'
                f'<div style="display:flex;height:4px;margin-bottom:1.25rem;">'
                f'<div style="flex:1;background:#FF7A00;"></div>'
                f'<div style="flex:1;background:#FFFFFF;"></div>'
                f'<div style="flex:1;background:#059669;"></div>'
                f'</div>'
                f'<div style="font-size:1.1rem;font-weight:800;color:#0F172A;margin-bottom:0.4rem;">📋 Application Details: {form_title}</div>'
                f'<hr style="border:none;border-top:2px solid #10B981;margin-bottom:1.25rem;" />'
                f'<div style="border:1px solid #CBD5E1;border-radius:10px;overflow:hidden;margin-bottom:1.25rem;box-shadow:0 2px 8px rgba(0,0,0,0.04);">{grid_rows}</div>'
                f'<div style="background:#ECFDF5;border:1.5px solid #10B981;padding:0.9rem 1.25rem;border-radius:10px;margin-bottom:1.25rem;">'
                f'<div style="font-weight:800;font-size:0.92rem;color:#065F46;margin-bottom:0.25rem;">📜 Applicant Self-Declaration & Authenticity Verification</div>'
                f'<div style="font-size:0.85rem;color:#047857;line-height:1.5;">I hereby declare that all information provided above is true and correct to the best of my knowledge. Verified & submitted via Formitra AI Multilingual Engine.</div>'
                f'</div>'
                f'<div style="text-align:center;padding:0.75rem;background:#F1F5F9;border-radius:8px;font-size:0.85rem;color:#334155;font-weight:700;border:1px dashed #94A3B8;">✅ Official Formitra Digital Application Receipt | Ref: <b>{ref_code}</b> | Verified & Sealed Electronically</div>'
                f'</div></body></html>'
            )
            components.html(card_html, height=720, scrolling=True)

    # Action Buttons: Download PDF, Track Status, Start New
    c1, c2, c3 = st.columns(3)
    with c1:
        if pdf_res:
            st.download_button(
                label=t("btn_download_pdf"),
                data=pdf_res.pdf_bytes,
                file_name=pdf_res.filename,
                mime="application/pdf",
                use_container_width=True,
                type="primary",
            )
    with c2:
        if st.button(t("btn_track_status"), use_container_width=True):
            session.navigate("track_status")
    with c3:
        if st.button(t("btn_start_new"), use_container_width=True):
            session.full_reset()
            session.navigate("home")

    spacer()
    info_box(f"💡 Preview your generated form above or click <b>'{t('btn_download_pdf')}'</b> to save a copy for your records. Reference Code: <b>{ref_code}</b>.")
