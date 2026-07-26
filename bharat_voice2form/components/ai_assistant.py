"""
components/ai_assistant.py
===========================
Animated Floating AI Assistant Widget for Formitra.
Renders on every page with page-contextual voice help and interactive guidance.
"""

from __future__ import annotations

import streamlit as st
from utils.translations import t
from utils.voice_assist  import render_voice_assistant_player
import utils.session as session

# Contextual tips per page key
_PAGE_TIPS: dict[str, tuple[str, str]] = {
    "home": (
        "Welcome to Formitra! I am your AI assistant. Click 'Select Form' to choose your scholarship application.",
        "स्वागत है! 'फॉर्म चुनें' पर क्लिक करके छात्रवृत्ति आवेदन शुरू करें।",
    ),
    "form_selection": (
        "Choose the scholarship scheme that matches your study level and click 'Start Voice Application'.",
        "अपनी अध्ययन स्तर के अनुसार छात्रवृत्ति योजना चुनें और वॉइस आवेदन शुरू करें।",
    ),
    "voice_input": (
        "Click 'Start Live Dictation' or use the audio recorder. Speak your Name, City, State, Course, Year & Income.",
        "माइक बटन दबाएं और अपना नाम, शहर, राज्य, कोर्स, वर्ष और आय स्पष्ट रूप से बोलें।",
    ),
    "ai_processing": (
        "Gemma AI is extracting your speech data and checking eligibility across government schemes.",
        "Gemma AI आपके भाषण डेटा को एक्सट्रैक्ट कर रही है और छात्रवृत्ति पात्रता जांच रही है।",
    ),
    "auto_fill": [
        "Review pre-filled fields. You can click the mic 🎙️ next to any individual input box to speak into that field!",
        "अपनी जानकारी जांचें। किसी भी फ़ील्ड के पास बने माइक 🎙️ पर क्लिक करके उसमें बोल सकते हैं!",
    ],
    "preview": (
        "Check your official scholarship form summary before final submission.",
        "अंतिम सबमिशन से पहले अपने आधिकारिक छात्रवृत्ति फॉर्म सारांश की समीक्षा करें।",
    ),
    "success": (
        "Your form is submitted! Save your Reference Number to track application status anytime.",
        "आपका फॉर्म जमा हो गया है! स्थिति ट्रैक करने के लिए अपना संदर्भ नंबर सहेजें।",
    ),
    "track_status": (
        "Enter your Formitra Reference Number (e.g., FMT-2026-89412) to check your application status.",
        "आवेदन की स्थिति जांचने के लिए अपना संदर्भ नंबर (जैसे FMT-2026-89412) दर्ज करें।",
    ),
    "help_faq": (
        "Browse common questions or ask me anything about scholarship eligibility and voice commands.",
        "छात्रवृत्ति पात्रता और आवाज़ से फॉर्म भरने के बारे में प्रश्न पूछें।",
    ),
}


def render_ai_assistant_widget() -> None:
    """Render floating animated AI assistant avatar widget."""
    current_page = session.get("current_page", "home")
    language     = session.get("selected_language", "Hindi")

    tip_en, tip_hi = _PAGE_TIPS.get(current_page, _PAGE_TIPS["home"])
    active_tip = tip_hi if language == "Hindi" else tip_en

    with st.expander("🤖 Formitra AI Assistant (Click for Page Help & Voice Guidance)", expanded=False):
        c1, c2 = st.columns([1, 4])
        with c1:
            st.markdown(
                '<div style="text-align:center;font-size:3rem;animation:bounce 1.5s infinite;">'
                '🤖</div>',
                unsafe_allow_html=True,
            )
        with c2:
            st.markdown(
                f'<div style="font-weight:700;font-size:0.95rem;color:#FF7A00;">'
                f'Formitra AI Assistant ({language})</div>'
                f'<div style="font-size:0.88rem;color:#475569;margin-top:0.25rem;">'
                f'{active_tip}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
            render_voice_assistant_player(
                text=active_tip,
                language=language,
                label=f"🔊 Speak Assistance ({language})",
            )
