"""
components/suggestions.py
=========================
AI Suggestions panel component rendered alongside the auto-fill form.

To update suggestion logic when Gemma is integrated:
  - Replace the static AI_SUGGESTIONS list in utils/constants.py
    with dynamically generated suggestions from gemma_processor output.
  - Call render_panel(suggestions=dynamic_list) to override defaults.
"""

from __future__ import annotations

import streamlit as st

from components.cards import suggestion_card
from components.progress import completion_meter
from utils.constants import AI_SUGGESTIONS


def render_panel(
    suggestions: list[dict] | None = None,
    extracted: dict | None = None,
    total_fields: int = 15,
) -> None:
    """
    Render the full AI Suggestions panel.

    Parameters
    ----------
    suggestions : list[dict] | None
        Override the default suggestion list.
        Each dict must have keys: icon, title, body, color.
    extracted : dict | None
        AI-extracted data dict — used to compute the completion meter.
        If None, detected count defaults to 0.
    total_fields : int
        Total number of fields in the form (for the completion meter).
    """
    st.markdown(
        '<div style="font-size:1.1rem;font-weight:700;color:#111827;margin-bottom:0.75rem;">'
        '🤖 AI Suggestions</div>'
        '<div style="font-size:0.85rem;color:#6B7280;margin-bottom:1rem;">'
        'Gemma recommends the following</div>',
        unsafe_allow_html=True,
    )

    items = suggestions or AI_SUGGESTIONS
    for s in items:
        suggestion_card(
            icon=s["icon"],
            title=s["title"],
            body=s["body"],
            color=s["color"],
        )

    # Completion meter
    detected = _count_detected(extracted or {})
    completion_meter(detected=detected, total=total_fields)


# ─── Private helpers ───────────────────────────────────────────────

_DETECTED_KEYS = ["Name", "City", "State", "Course", "Year", "Income"]


def _count_detected(extracted: dict) -> int:
    """Count how many key fields were successfully extracted."""
    return sum(1 for k in _DETECTED_KEYS if extracted.get(k))
