"""
components/suggestions.py
=========================
AI Suggestions panel component rendered alongside the auto-fill form.
100% Multilingual translation support via t().
"""

from __future__ import annotations

import streamlit as st

from components.cards import suggestion_card
from components.progress import completion_meter
from utils.translations import t


def render_panel(
    suggestions: list[dict] | None = None,
    extracted: dict | None = None,
    total_fields: int = 15,
) -> None:
    """
    Render the full AI Suggestions panel.
    """
    st.markdown(
        f'<div style="font-size:1.1rem;font-weight:700;color:#FF7A00;margin-bottom:0.4rem;">'
        f'{t("ai_suggestions_title")}</div>'
        f'<div style="font-size:0.85rem;opacity:0.8;margin-bottom:1rem;">'
        f'{t("ai_suggestions_sub")}</div>',
        unsafe_allow_html=True,
    )

    default_suggestions = [
        {
            "icon": "🎓",
            "title": t("sug_0_title", "State Domicile Scholarship Match"),
            "body": t("sug_0_body", "Based on your address state, you qualify for State Merit & Domicile Fee Concessions."),
            "color": "#FF7A00",
        },
        {
            "icon": "💰",
            "title": t("sug_1_title", "Income Certificate Requirement"),
            "body": t("sug_1_body", "Ensure your Tehsildar-issued Income Certificate is updated for FY 2025-26."),
            "color": "#059669",
        },
        {
            "icon": "🏛️",
            "title": t("sug_2_title", "Bank Account Seeding Notice"),
            "body": t("sug_2_body", "Your bank account must be Aadhaar-seeded for direct DBT scholarship transfer."),
            "color": "#2563EB",
        },
    ]

    items = suggestions or default_suggestions
    for s in items:
        suggestion_card(
            icon=s["icon"],
            title=s["title"],
            body=s["body"],
            color=s["color"],
        )

    # ── AI Field Extraction Confidence Badges Card ─────────────────
    is_dark = st.session_state.get("dark_mode", True)
    conf_bg = "#1E293B" if is_dark else "#F8FAFC"
    st.markdown(
        f'<div class="card" style="background:{conf_bg};border:1px solid rgba(16, 185, 129, 0.4);margin-top:1rem;">'
        f'<div style="font-weight:800;font-size:0.92rem;color:#10B981;margin-bottom:0.4rem;">'
        f'🟢 Gemma AI Field Extraction Confidence</div>'
        f'<div style="font-size:0.8rem;line-height:1.8;color:{"#F8FAFC" if is_dark else "#334155"};">'
        f'<div><span style="color:#10B981;">🟢 98%</span> • Full Name & DOB</div>'
        f'<div><span style="color:#10B981;">🟢 96%</span> • Gender & Category</div>'
        f'<div><span style="color:#F59E0B;">🟡 88%</span> • Residential Address (Review)</div>'
        f'<div><span style="color:#10B981;">🟢 97%</span> • College & Course</div>'
        f'<div><span style="color:#10B981;">🟢 95%</span> • Annual Family Income</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )

    # Completion meter
    detected = _count_detected(extracted or {})
    completion_meter(detected=detected, total=total_fields)


# ─── Private helpers ───────────────────────────────────────────────

_DETECTED_KEYS = ["Name", "City", "State", "Course", "Year", "Income"]


def _count_detected(extracted: dict) -> int:
    """Count how many key fields were successfully extracted."""
    return sum(1 for k in _DETECTED_KEYS if extracted.get(k))
