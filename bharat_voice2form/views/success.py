"""
views/success.py
=================
Submission success page for Formitra.
Features stunning celebratory confetti & badge animations upon form submission.
"""

import random
import streamlit as st

from components.layout   import tricolour_bar, section_heading, info_box, spacer
from components.progress import step_progress_bar
from utils.translations  import t
from utils.voice_assist  import render_voice_assistant_player
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
    language   = session.get("selected_language", "Hindi")

    # ── Celebration HTML/CSS Confetti & Pulse Animation ─────────────
    animation_html = f"""
    <style>
        .celebration-container {{
            background: linear-gradient(135deg, #065F46 0%, #047857 50%, #064E3B 100%);
            border-radius: 24px;
            padding: 3rem 2rem;
            color: #FFFFFF;
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
        <!-- Confetti Particles -->
        <div class="confetti-particle" style="left:10%;animation-delay:0s;background:#FBBF24;"></div>
        <div class="confetti-particle" style="left:25%;animation-delay:0.4s;background:#34D399;"></div>
        <div class="confetti-particle" style="left:40%;animation-delay:0.8s;background:#F472B6;"></div>
        <div class="confetti-particle" style="left:60%;animation-delay:0.2s;background:#60A5FA;"></div>
        <div class="confetti-particle" style="left:75%;animation-delay:0.6s;background:#FBBF24;"></div>
        <div class="confetti-particle" style="left:90%;animation-delay:1s;background:#A7F3D0;"></div>

        <div class="badge-ripple">✅</div>
        <div style="font-size:2.2rem;font-weight:900;letter-spacing:-0.5px;color:#FFFFFF;">
            Application Submitted Successfully!
        </div>
        <div style="font-size:1.05rem;color:#D1FAE5;margin-top:0.5rem;">
            Your voice-assisted application for <b>{form_title}</b> is complete & logged.
        </div>
        
        <div style="margin-top:1.75rem;display:inline-block;background:rgba(255, 255, 255, 0.15);backdrop-filter:blur(8px);padding:1rem 2.2rem;border-radius:50px;border:2px dashed #A7F3D0;">
            <span style="font-size:0.85rem;color:#E6F4EA;font-weight:700;">FORMITRA REFERENCE CODE: </span>
            <span style="font-size:1.5rem;font-weight:900;color:#FDE047;letter-spacing:1.5px;">{ref_code}</span>
        </div>
    </div>
    """
    st.markdown(animation_html, unsafe_allow_html=True)

    # Voice Speech Announcement
    tts_text = f"Congratulations! Your application for {form_title} has been submitted successfully. Your reference code is {ref_code}."
    render_voice_assistant_player(text=tts_text, language=language, label=f"🔊 Listen to Submission Confirmation ({language})")

    spacer()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔍 Track Application Status", use_container_width=True, type="primary"):
            session.navigate("track_status")
    with c2:
        if st.button("🔄 Start New Application", use_container_width=True):
            session.reset_all()
            session.navigate("home")

    spacer()
    info_box(f"💡 Save your Reference Code <b>{ref_code}</b>. You can use it anytime on the 'Track Status' page to check verification progress and print your application receipt.")
