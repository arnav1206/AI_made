"""
views/success.py
=================
Submission success page for Formitra.
100% Multilingual translation support via t().
Features celebratory green badge animation, ref code display, live document preview & download option.
"""

import base64
import random
import streamlit as st

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.translations  import t
from utils.voice_assist  import render_voice_assistant_player
from utils.pdf_generator import generate as generate_pdf
import utils.session as session


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

    form_title = session.get("selected_form") or "Scholarship Application"
    language   = session.get("selected_language", "Hindi")
    form_data  = session.get("form_data", {})

    # Generate PDF document for preview & download
    pdf_res = generate_pdf(
        form_data=form_data,
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

    # Live Interactive Document Preview Box
    if pdf_res:
        with st.expander(t("preview_doc_title"), expanded=True):
            b64_pdf = base64.b64encode(pdf_res.pdf_bytes).decode("utf-8")
            
            grid_items = "".join(
                f'<div style="display:flex;justify-content:space-between;padding:0.45rem 0.8rem;border-bottom:1px solid #E2E8F0;'
                f'background:{"#F8FAFC" if idx % 2 == 0 else "#FFFFFF"};">'
                f'<span style="font-weight:700;color:#0F172A;font-size:0.85rem;">{k}:</span>'
                f'<span style="color:#334155;font-size:0.85rem;">{v or "—"}</span></div>'
                for idx, (k, v) in enumerate(form_data.items())
            ) if form_data else ""

            doc_fallback = f"""
            <object data="data:application/pdf;base64,{b64_pdf}" type="application/pdf" width="100%" height="450" style="border:1.5px solid #10B981;border-radius:12px;">
                <div style="background:#FFFFFF;color:#0F172A;padding:1.5rem;border-radius:12px;border:2px solid #059669;">
                    <div style="background:#0F172A;color:#FFFFFF;padding:1rem;border-radius:8px;margin-bottom:0.75rem;">
                        <div style="font-weight:800;font-size:1.1rem;color:#FF7A00;">NATIONAL SCHOLARSHIP PORTAL — GOVT OF INDIA</div>
                        <div style="font-size:0.85rem;color:#E2E8F0;">Formitra AI Voice Application Receipt | Ref: {ref_code}</div>
                    </div>
                    <div style="margin-bottom:1rem;">{grid_items}</div>
                    <div style="background:#ECFDF5;border:1px solid #10B981;padding:0.75rem;border-radius:6px;font-size:0.8rem;color:#065F46;">
                        <b>{t("receipt_sealed")}</b>
                    </div>
                </div>
            </object>
            """
            st.markdown(doc_fallback, unsafe_allow_html=True)

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
