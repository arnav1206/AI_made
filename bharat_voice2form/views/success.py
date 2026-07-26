"""
views/success.py
=================
Submission success page for Formitra.
Generates an official Reference Tracking Code (e.g. FMT-2026-89412).
"""

import random
import streamlit as st

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.translations  import t
import utils.session as session


def render() -> None:
    tricolour_bar()
    step_progress_bar(current_step=6)

    # Generate or retrieve unique reference tracking code
    if not session.get("reference_code"):
        code_num = random.randint(10000, 99999)
        ref_code = f"FMT-2026-{code_num}"
        session.set("reference_code", ref_code)
        session.set("active_ref_code", ref_code)
    else:
        ref_code = session.get("reference_code")

    form_title = session.get("selected_form", "Scholarship Application")

    st.markdown(
        f'<div style="background:linear-gradient(135deg,#ECFDF5,#D1FAE5);'
        f'border-radius:24px;padding:2.5rem;text-align:center;border:2px solid #A7F3D0;'
        f'box-shadow:0 15px 35px rgba(5,150,105,0.15);margin-bottom:2rem;">'
        f'<div style="font-size:3.5rem;margin-bottom:0.5rem;">🎉</div>'
        f'<div style="font-size:1.8rem;font-weight:900;color:#065F46;">'
        f'Application Submitted Successfully!</div>'
        f'<div style="font-size:1rem;color:#047857;margin-top:0.4rem;">'
        f'Your voice-filled application for <b>{form_title}</b> has been received and logged.</div>'
        f'<div style="margin-top:1.5rem;display:inline-block;background:#FFFFFF;'
        f'padding:0.9rem 2rem;border-radius:50px;border:2px dashed #059669;">'
        f'<span style="font-size:0.85rem;color:#64748B;font-weight:700;">FORMITRA REFERENCE NUMBER: </span>'
        f'<span style="font-size:1.4rem;font-weight:900;color:#059669;letter-spacing:1px;">{ref_code}</span>'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 Track Application Status", use_container_width=True, type="primary"):
            session.navigate("track_status")
    with c2:
        if st.button("🔄 Start New Application", use_container_width=True):
            session.reset_all()
            session.navigate("home")

    spacer()
    info_box(f"💡 Save your Reference Code <b>{ref_code}</b>. You can use it anytime on the 'Track / Login' page to check verification status and print your application receipt.")
